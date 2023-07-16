targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

// Prompt user for apimEndpoint, apimKey, and serviceName if not provided
@description('API-M endpoint')
param apimEndpoint string 

// Make this one secure as it's a key
@secure()
@description('API-M key')
param apimKey string

@description('Name of the web app and web service')
param serviceName string = 'aoai-streamlit-app'

@description('Azure OpenAI API version')
param aoaiApiVersion string = '2023-05-15'

@minLength(1)
@description('Primary location for all resources')
param location string

param appServicePlanName string = ''
param resourceGroupName string = ''
param webServiceName string = ''

// Load the abbreviations.json file to use in resource names
var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// Create an App Service Plan to group applications under the same payment plan and SKU
// aoai-streamlit-app\infra\core
module appServicePlan '../infra/core/host/appserviceplan.bicep' = {
  name: 'appserviceplan'
  scope: rg
  params: {
    name: !empty(appServicePlanName) ? appServicePlanName : '${abbrs.webServerFarms}${resourceToken}'
    location: location
    tags: tags
    sku: {
      name: 'P1v3'
    }
    kind: 'linux'
    reserved: true
  }
}

// The application frontend
module web './core/host/appservice.bicep' = {
  name: serviceName
  scope: rg
  params: {
    name: !empty(webServiceName) ? webServiceName : '${abbrs.webSitesAppService}web-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    appServicePlanId: appServicePlan.outputs.id
    runtimeName: 'python'
    runtimeVersion: '3.11'
    scmDoBuildDuringDeployment: true
    appCommandLine: 'python -m streamlit run aoai_streamlit_app.py --server.port 8000 --server.address 0.0.0.0' // Add these back at some point to pass as parameters to the aoai_streamlit_app.py file --apim-endpoint ${apimEndpoint} --apim-key ${apimKey}'
    // Add environment variables
    appSettings: {
      APIM_ENDPOINT: apimEndpoint
      APIM_KEY: apimKey
      AOAI_API_VERSION: aoaiApiVersion
    }
  }
}

// App outputs
output AZURE_TENANT_ID string = tenant().tenantId
output REACT_APP_WEB_BASE_URL string = web.outputs.uri
output resourceGroupName string = rg.name
output webServiceName string = web.name
