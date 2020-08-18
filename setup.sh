#!/bin/bash
set -x

#1 env(environment), 3 app(application name),
#4 config_branch(used only in the dev-environment), 5 deployment type: app/worker/cron
#environment possible values: local, dev, staging, production
export ENV="$1"
export APP="$2"
export FUNCTION="${3:-all}"

echo "Environment used: $ENV"
echo "App: $APP"
echo "App: $FUNCTION"


cd ${APP}
npm install
if [[ $FUNCTION != "all" ]]; then
    echo "Deploying Single function $FUNCTION"
    serverless deploy --stage ${ENV} -f ${FUNCTION}
else
    echo "Deploying All functions"
    serverless deploy --stage ${ENV}
fi
cd ..
