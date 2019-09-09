aws cloudformation create-stack \
--stack-name deploy-pipeline \
--template-body file://deploy_pipeline.yaml \
--capabilities CAPABILITY_IAM \
--parameters file://parameters.json