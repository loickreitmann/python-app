#!/usr/bin/env bash

set -e

NAMESPACE="argocd"
PORT=8080
USERNAME="admin"

echo "🔁 Starting port-forward to Argo CD server..."
kubectl port-forward svc/argocd-server -n $NAMESPACE $PORT:80 > /tmp/argocd-portforward.log 2>&1 &

PF_PID=$!

# Ensure we kill the port-forward on exit
trap "echo '🛑 Killing port-forward (PID $PF_PID)'; kill $PF_PID" EXIT

# Wait for the port to become available
echo "⏳ Waiting for port $PORT to be available..."
for i in {1..10}; do
  if nc -z localhost $PORT; then
    break
  fi
  sleep 1
done

if ! nc -z localhost $PORT; then
  echo "❌ Port-forward failed to start."
  kill $PF_PID
  exit 1
fi

echo "✅ Port-forward established."

# Get the admin password
echo "🔐 Getting Argo CD admin password..."
PASSWORD=$ARGOCD_ADMIN_PASSWORD

echo "🔑 Logging in to Argo CD CLI at localhost:$PORT..."
argocd login localhost:$PORT --username $USERNAME --password "$PASSWORD" --insecure --skip-test-tls

echo "🎉 Logged in to Argo CD CLI!"

# Keep port-forward running in foreground (optional)
wait $PF_PID
