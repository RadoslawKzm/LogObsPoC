# Internal Error Code Documentation

## 📘 Table of Contents

- [1xxx Auth Codes](#1xxx-auth-codes)
  - [11xx Authentication Codes](#11xx-authentication-codes)
  - [12xx Authorization Codes](#12xx-authorization-codes)
- [2xxx Api Codes](#2xxx-api-codes)
  - [21xx InvalidInput Codes](#21xx-invalidinput-codes)
  - [22xx UnknownServer Codes](#22xx-unknownserver-codes)
- [3xxx Core Codes](#3xxx-core-codes)
- [4xxx Db Codes](#4xxx-db-codes)
  - [41xx SQL Codes](#41xx-sql-codes)
  - [42xx Mongo Codes](#42xx-mongo-codes)
  - [43xx FileStorage Codes](#43xx-filestorage-codes)
- [5xxx Cloud Codes](#5xxx-cloud-codes)
  - [51xx AWS Codes](#51xx-aws-codes)
  - [52xx Azure Codes](#52xx-azure-codes)
  - [53xx GCP Codes](#53xx-gcp-codes)
  - [54xx OnPrem Codes](#54xx-onprem-codes)


- [📄 Code Explanations](#-code-explanations)
---
## 1xxx Auth Codes
  - `1000` Auth Base Code | HTTP 401 | [Details](#code-1000)
      - ### 11xx Authentication Codes
      - `1100` Authentication | HTTP 401 | [Details](#code-1100)]
      - `1101` Unauthorized | HTTP 401 | [Details](#code-1101)]
      - `1102` SessionExpired | HTTP 401 | [Details](#code-1102)]
      - ### 12xx Authorization Codes
      - `1200` Authorization | HTTP 403 | [Details](#code-1200)]
      - `1201` Forbidden | HTTP 403 | [Details](#code-1201)]
## 2xxx Api Codes
  - `2000` Api Base Code | HTTP 500 | [Details](#code-2000)
      - ### 21xx InvalidInput Codes
      - `2100` InvalidInput | HTTP 400 | [Details](#code-2100)]
      - `2101` MissingField | HTTP 400 | [Details](#code-2101)]
      - `2102` FieldFormat | HTTP 400 | [Details](#code-2102)]
      - `2103` NotFound | HTTP 404 | [Details](#code-2103)]
      - `2104` RequestConflict | HTTP 409 | [Details](#code-2104)]
      - ### 22xx UnknownServer Codes
      - `2200` UnknownServer | HTTP 500 | [Details](#code-2200)]
      - `2201` ExternalServiceUnavailable | HTTP 503 | [Details](#code-2201)]
      - `2202` RequestTimeout | HTTP 504 | [Details](#code-2202)]
      - `2203` Configuration | HTTP 500 | [Details](#code-2203)]
## 3xxx Core Codes
  - `3000` Core Base Code | HTTP 500 | [Details](#code-3000)
    - `3001` Unexpected | HTTP 500 | [Details](#code-3001)]
    - `3002` Configuration | HTTP 500 | [Details](#code-3002)]
    - `3003` ResourceConflict | HTTP 409 | [Details](#code-3003)]
    - `3004` ExternalService | HTTP 502 | [Details](#code-3004)]
    - `3005` Timeout | HTTP 504 | [Details](#code-3005)]
    - `3006` DataInconsistency | HTTP 500 | [Details](#code-3006)]
    - `3007` FeatureDisabled | HTTP 503 | [Details](#code-3007)]
## 4xxx Db Codes
  - `4000` Db Base Code | HTTP 500 | [Details](#code-4000)
      - ### 41xx SQL Codes
      - `4100` SQL | HTTP 500 | [Details](#code-4100)]
      - `4101` Conn | HTTP 503 | [Details](#code-4101)]
      - `4102` Integrity | HTTP 500 | [Details](#code-4102)]
      - `4103` Data | HTTP 400 | [Details](#code-4103)]
      - `4104` Operational | HTTP 503 | [Details](#code-4104)]
      - `4105` Programming | HTTP 500 | [Details](#code-4105)]
      - `4106` InvalidRequest | HTTP 400 | [Details](#code-4106)]
      - `4107` Database | HTTP 500 | [Details](#code-4107)]
      - ### 42xx Mongo Codes
      - `4200` Mongo | HTTP 500 | [Details](#code-4200)]
      - `4201` Example | HTTP 500 | [Details](#code-4201)]
      - ### 43xx FileStorage Codes
      - `4300` FileStorage | HTTP 500 | [Details](#code-4300)]
      - `4301` FileNotFound | HTTP 404 | [Details](#code-4301)]
      - `4302` FileAlreadyExists | HTTP 409 | [Details](#code-4302)]
      - `4303` FileRead | HTTP 500 | [Details](#code-4303)]
      - `4304` FileWrite | HTTP 500 | [Details](#code-4304)]
      - `4305` FileUpdate | HTTP 500 | [Details](#code-4305)]
      - `4306` FileDelete | HTTP 500 | [Details](#code-4306)]
      - `4307` FileList | HTTP 500 | [Details](#code-4307)]
## 5xxx Cloud Codes
  - `5000` Cloud Base Code | HTTP 500 | [Details](#code-5000)
      - ### 51xx AWS Codes
      - `5100` AWS | HTTP 500 | [Details](#code-5100)]
      - `5101` AWSPermissionDenied | HTTP 403 | [Details](#code-5101)]
      - `5102` AWSServiceTimeout | HTTP 504 | [Details](#code-5102)]
      - `5103` AWSRateLimitExceeded | HTTP 429 | [Details](#code-5103)]
      - ### 52xx Azure Codes
      - `5200` Azure | HTTP 500 | [Details](#code-5200)]
      - `5201` AzureAuthentication | HTTP 401 | [Details](#code-5201)]
      - `5202` AzureResourceUnavailable | HTTP 503 | [Details](#code-5202)]
      - ### 53xx GCP Codes
      - `5300` GCP | HTTP 500 | [Details](#code-5300)]
      - `5301` GCPAuthentication | HTTP 401 | [Details](#code-5301)]
      - `5302` GCPQuotaExceeded | HTTP 429 | [Details](#code-5302)]
      - `5303` GCPServiceUnavailable | HTTP 503 | [Details](#code-5303)]
      - ### 54xx OnPrem Codes
      - `5400` OnPrem | HTTP 500 | [Details](#code-5400)]
      - `5401` Test | HTTP 500 | [Details](#code-5401)]


---


# 📄 Code Explanations

### Auth Codes
#### <a id='code-1000'></a> `1000` AuthError
General AuthError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### Authentication Codes
#### <a id='code-1100'></a> `1100` AuthenticationError
General AuthenticationError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-1101'></a> `1101` UnauthorizedError
Invalid or missing authentication.<br>
_Probable cause: Missing or invalid authentication token._
#### <a id='code-1102'></a> `1102` SessionExpiredError
Session expired. Please log in again.<br>
_Probable cause: User session or token has expired._
#### Authorization Codes
#### <a id='code-1200'></a> `1200` AuthorizationError
General AuthorizationError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-1201'></a> `1201` ForbiddenError
You do not have permission to access this resource.<br>
_Probable cause: User lacks sufficient permissions._
### Api Codes
#### <a id='code-2000'></a> `2000` ApiError
General ApiError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### InvalidInput Codes
#### <a id='code-2100'></a> `2100` InvalidInputError
General InvalidInputError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-2101'></a> `2101` MissingFieldError
Missing required field.<br>
_Probable cause: Mandatory field missing in request payload._
#### <a id='code-2102'></a> `2102` FieldFormatError
Incorrect field format.<br>
_Probable cause: One or more fields violate validation rules._
#### <a id='code-2103'></a> `2103` NotFoundError
Requested resource not found.<br>
_Probable cause: Resource does not exist or is inaccessible._
#### <a id='code-2104'></a> `2104` RequestConflictError
Request conflict.<br>
_Probable cause: Request conflicts with the current resource state._
#### UnknownServer Codes
#### <a id='code-2200'></a> `2200` UnknownServerError
General UnknownServerError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-2201'></a> `2201` ExternalServiceUnavailableError
External service unavailable.<br>
_Probable cause: Dependent external service is down or unreachable._
#### <a id='code-2202'></a> `2202` RequestTimeoutError
Request timed out.<br>
_Probable cause: API request exceeded timeout while waiting for a response._
#### <a id='code-2203'></a> `2203` ConfigurationError
Configuration error.<br>
_Probable cause: API configuration or environment is invalid or missing._
### Core Codes
#### <a id='code-3000'></a> `3000` CoreError
General CoreError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-3001'></a> `3001` UnexpectedError
Unexpected error.<br>
_Probable cause: Unhandled failure in core logic._
#### <a id='code-3002'></a> `3002` ConfigurationError
Configuration error.<br>
_Probable cause: Critical configuration value missing or invalid._
#### <a id='code-3003'></a> `3003` ResourceConflictError
Resource conflict.<br>
_Probable cause: Conflict with current resource state due to concurrency or version mismatch._
#### <a id='code-3004'></a> `3004` ExternalServiceError
External service error.<br>
_Probable cause: Failed communication with an upstream dependency._
#### <a id='code-3005'></a> `3005` TimeoutError
Request timed out.<br>
_Probable cause: Request exceeded the allowed time limit._
#### <a id='code-3006'></a> `3006` DataInconsistencyError
Data inconsistency detected.<br>
_Probable cause: Application-level integrity or consistency check failed._
#### <a id='code-3007'></a> `3007` FeatureDisabledError
Feature temporarily disabled.<br>
_Probable cause: Feature has been disabled by system configuration._
### Db Codes
#### <a id='code-4000'></a> `4000` DbError
General DbError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### SQL Codes
#### <a id='code-4100'></a> `4100` SQLError
General SQLError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-4101'></a> `4101` ConnError
Temporary issue. Please try again shortly.<br>
_Probable cause: Failed to establish a connection to the SQL database._
#### <a id='code-4102'></a> `4102` IntegrityError
A data error occurred. Please contact support.<br>
_Probable cause: Integrity constraint violated (foreign key, unique)._
#### <a id='code-4103'></a> `4103` DataError
Invalid data provided.<br>
_Probable cause: Sent data is invalid or incompatible with schema._
#### <a id='code-4104'></a> `4104` OperationalError
Temporary service issue. Try again later.<br>
_Probable cause: DB operation failed due to I/O or connection issue._
#### <a id='code-4105'></a> `4105` ProgrammingError
Something went wrong. Please try again later.<br>
_Probable cause: SQL statement contains a programming or syntax error._
#### <a id='code-4106'></a> `4106` InvalidRequestError
The request was invalid or unsupported.<br>
_Probable cause: SQL operation was malformed or unsupported._
#### <a id='code-4107'></a> `4107` DatabaseError
An unexpected database error occurred.<br>
_Probable cause: Parent class of SQLAlchemy exceptions._
#### Mongo Codes
#### <a id='code-4200'></a> `4200` MongoError
General MongoError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-4201'></a> `4201` ExampleError
Unexpected error. We're looking into it.<br>
_Probable cause: ('Base unexpected MongoDB exception. ', 'If visible in logs, something went uncaught.')_
#### FileStorage Codes
#### <a id='code-4300'></a> `4300` FileStorageError
General FileStorageError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-4301'></a> `4301` FileNotFound
The requested file was not found.<br>
_Probable cause: File does not exist in the data storage folder._
#### <a id='code-4302'></a> `4302` FileAlreadyExists
The file already exists.<br>
_Probable cause: Attempted to create a file that already exists._
#### <a id='code-4303'></a> `4303` FileReadError
Unable to read the file.<br>
_Probable cause: Error occurred while reading the file from storage._
#### <a id='code-4304'></a> `4304` FileWriteError
Unable to write to the file.<br>
_Probable cause: Error occurred while writing content to the file._
#### <a id='code-4305'></a> `4305` FileUpdateError
Unable to update the file.<br>
_Probable cause: Error occurred while updating or appending content to the file._
#### <a id='code-4306'></a> `4306` FileDeleteError
Unable to delete the file.<br>
_Probable cause: Error occurred while deleting the file from storage._
#### <a id='code-4307'></a> `4307` FileListError
Unable to list files.<br>
_Probable cause: Error occurred while listing files in the data storage folder._
### Cloud Codes
#### <a id='code-5000'></a> `5000` CloudError
General CloudError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### AWS Codes
#### <a id='code-5100'></a> `5100` AWSError
General AWSError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-5101'></a> `5101` AWSPermissionDeniedError
Permission denied for AWS operation.<br>
_Probable cause: Insufficient AWS IAM permissions._
#### <a id='code-5102'></a> `5102` AWSServiceTimeoutError
Timeout while communicating with AWS service.<br>
_Probable cause: AWS service did not respond within the timeout window._
#### <a id='code-5103'></a> `5103` AWSRateLimitExceededError
AWS rate limit exceeded.<br>
_Probable cause: Too many requests to AWS service in a short time._
#### Azure Codes
#### <a id='code-5200'></a> `5200` AzureError
General AzureError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-5201'></a> `5201` AzureAuthenticationError
Failed to authenticate with Azure cloud.<br>
_Probable cause: Azure credentials invalid or expired._
#### <a id='code-5202'></a> `5202` AzureResourceUnavailableError
Azure resource is temporarily unavailable.<br>
_Probable cause: Azure resource could not be reached or is down._
#### GCP Codes
#### <a id='code-5300'></a> `5300` GCPError
General GCPError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-5301'></a> `5301` GCPAuthenticationError
Failed to authenticate with Google Cloud.<br>
_Probable cause: GCP credentials invalid or expired._
#### <a id='code-5302'></a> `5302` GCPQuotaExceededError
Quota exceeded on Google Cloud service.<br>
_Probable cause: GCP quota exceeded for this operation._
#### <a id='code-5303'></a> `5303` GCPServiceUnavailableError
Google Cloud service is temporarily unavailable.<br>
_Probable cause: Service down or unreachable on GCP._
#### OnPrem Codes
#### <a id='code-5400'></a> `5400` OnPremError
General OnPremError Base Error.<br>
_Probable cause: Unexpected and Uncaught base exception_
#### <a id='code-5401'></a> `5401` TestError
Internal server error. Our team has been notified.<br>
_Probable cause: Unexpected error while communicating with internal infrastructure._