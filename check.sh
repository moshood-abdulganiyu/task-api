#!/bin/bash
BASE=http://localhost:8000
code() { curl -s -o /dev/null -w "%{http_code}\n" "$@"; }

echo "GET /tasks (200):";        code $BASE/tasks
echo "GET /tasks/1 (200):";      code $BASE/tasks/1
echo "GET /tasks/999 (404):";    code $BASE/tasks/999
echo "POST ok (201):";           code -X POST $BASE/tasks -H "Content-Type: application/json" -d '{"title":"check"}'
echo "POST bad (400):";          code -X POST $BASE/tasks -H "Content-Type: application/json" -d '{}'
echo "DELETE missing (404):";    code -X DELETE $BASE/tasks/999