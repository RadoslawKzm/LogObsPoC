# Internal Error Code Documentation

## 📘 Table of Contents

- [1xxx API Codes](#1xxx-api-codes)
  - [11xx Authentication / Authorization](#11xx-authentication--authorization)
  - [12xx Input / Validation](#12xx-input--validation-http4xx)
  - [13xx API Internal Server Errors](#13xx-api-internal-server-errors-http-5xx)
- [2xxxx Database Codes](#2xxxx-database-codes)
  - [21xxx SQL Codes](#21xxx-sql-codes)
    - [211xx Manual SQL codes](#211xx-manual-sql-codes-http-4xx)
    - [212xx Unexpected SQL codes](#212xx-unexpected-sql-codes-http-5xx)
  - [22xxx Mongo Codes](#22xxx-mongo-codes)
    - [221xx Manual Mongo codes](#221xx-manual-mongo-codes-http-4xx)
    - [222xx Unexpected Mongo Codes](#222xx-unexpected-mongo-codes-http-5xx)
- [3xxx Cloud Codes](#3xxx-cloud)
  - [31xx Azure Codes](#31xx-azure-codes)
  - [32xx AWS Codes](#32xx-aws-codes)
  - [33xx GCP Codes](#33xx-gcp-codes)
- [4xxx Reserved / Custom](#4xxx-reserved--custom)
  - [41xx Custom Business Logic](#41xx-custom-business-logic)
- [📄 Code Explanations](#code-explanations)

---

## 1xxx API codes
  - `1000` API base code | HTTP500 | [Details](#code-1000)
    - ### 11xx Authentication / Authorization (HTTP4xx)
    - `1100` Unauthorized | _HTTP 401_ | [Details](#code-1100)
    - `1101` Forbidden | _HTTP 403_ | [Details](#code-1101)
    - `1102` Session Expired | _HTTP 401_ | [Details](#code-1102)

    - ### 12xx Input / Validation (HTTP4xx)
    - `1200` Invalid Input | _HTTP 400_ | [Details](#code-1200)
    - `1201` Missing Required Field | _HTTP 400_ | [Details](#code-1201)
    - `1202` Field Format Error | _HTTP 400_ | [Details](#code-1202)
    - `1203` Resource Not Found | _HTTP 404_ | [Details](#code-1203)
    - `1204` Request Conflict | _HTTP 409_ | [Details](#code-1204)

    - ### 13xx API Internal Server Errors (HTTP 5xx)
    - `1300` Unknown Server Error | _HTTP 500_ | [Details](#code-1300)
    - `1301` External Service Unavailable | _HTTP 503_ | [Details](#code-1301)
    - `1302` Timeout | _HTTP 504_ | [Details](#code-1302)
    - `1303` Configuration Error | _HTTP 500_ | [Details](#code-1303)

---

## 2xxxx Database Codes
- ### 21xxx SQL Codes
  - #### 211xx Manual SQL codes (HTTP 4xx)
    - `21100` SQL Base Code | _HTTP 500_ | [Details](#code-21100)
    - `21101` Not Found | _HTTP 404_ | [Details](#code-21101)
    - `21102` Connection Error | _HTTP 503_ | [Details](#code-21102)
    - `21103` Resource Exists | _HTTP 400_ | [Details](#code-21103)
    - `21104` Resource Update Failed | _HTTP 400_ | [Details](#code-21104)
    - `21105` Deletion Failed | _HTTP 400_ | [Details](#code-21105)
    - `21106` Record Update Exists | _HTTP 400_ | [Details](#code-21106)
    - `21107` Requested Delete Not Found | _HTTP 404_ | [Details](#code-21107)

  - #### 212xx Unexpected SQL codes (HTTP 5xx)
    - `21201` Integrity Error | _HTTP 500_ | [Details](#code-21201)
    - `21202` Data Error | _HTTP 400_ | [Details](#code-21202)
    - `21203` Operational Error | _HTTP 503_ | [Details](#code-21203)
    - `21204` Programming Error | _HTTP 500_ | [Details](#code-21204)
    - `21205` Invalid Request | _HTTP 400_ | [Details](#code-21205)
    - `21206` Database error | _HTTP 500_ | [Details](#code-21206)

---

### 22xxx Mongo Codes
  - #### 221xx Manual Mongo codes (HTTP 4xx)
    - `22100` Mongo Base Code | _HTTP 500_ | [Details](#code-22100)
    - `22101` Not Found | _HTTP 404_ | [Details](#code-22101)
    - `22102` Connection Error | _HTTP 503_ | [Details](#code-22102)
    - `22103` Resource Exists | _HTTP 400_ | [Details](#code-22103)
    - `22104` Resource Update Failed | _HTTP 400_ | [Details](#code-22104)
    - `22105` Deletion Failed | _HTTP 400_ | [Details](#code-22105)
    - `22106` Record Update Exists | _HTTP 400_ | [Details](#code-22106)
    - `22107` Requested Delete Not Found | _HTTP 404_ | [Details](#code-22107)

  - #### 222xx Unexpected Mongo Codes (HTTP 5xx)
    - `22201` Integrity Error | _HTTP 500_ | [Details](#code-22201)
    - `22202` Data Error | _HTTP 400_ | [Details](#code-22202)
    - `22203` Operational Error | _HTTP 503_ | [Details](#code-22203)
    - `22204` Programming Error | _HTTP 500_ | [Details](#code-22204)
    - `22205` Invalid Request | _HTTP 400_ | [Details](#code-22205)

---

## 3xxx Cloud
  - ### 31xx Azure Codes
    - `31000` | Azure Base Error | Varies | [Details](#code-31000)
    - `31001` | Azure Authentication Failure | Varies | [Details](#code-31001)
    - `31002` | Azure Resource Not Available | Varies | [Details](#code-31002)

---

  - ### 32xx AWS Codes
    - `32000` | AWS Base Error | Varies | [Details](#code-32000)
    - `32001` | AWS Permission Denied | Varies | [Details](#code-32001)
    - `32002` | AWS Service Timeout | Varies | [Details](#code-32002)

---

  - ### 33xx GCP Codes
    - `33000` | GCP Base Error | Varies | [Details](#code-33000)
    - `33001` | GCP Authentication Failure | Varies | [Details](#code-33001)
    - `33002` | GCP Quota Exceeded | Varies | [Details](#code-33002)

---

## 4xxx Reserved / Custom
  - ### 41xx Custom Business Logic
    - `41101` Promotion Expired | _HTTP 400_ | [Details](#code-41101)
    - `41102` Payment Required | _HTTP 402_ | [Details](#code-41102)
    - `41103` Trial Limit Reached | _HTTP 403_ | [Details](#code-41103)

---

# 📄 Code Explanations

### API Codes

#### <a id="code-1000"></a>`1000` API Base Code  
General API failure indicating an unspecified server-side error.  
_Probable cause: Unexpected runtime exception or misconfiguration causing API to fail._

#### <a id="code-1100"></a>`1100` Unauthorized  
User is not authenticated or credentials are missing/invalid.  
_Probable cause: Missing/expired/invalid authentication token or session._

#### <a id="code-1101"></a>`1101` Forbidden  
User is authenticated but does not have permission to access the resource.  
_Probable cause: Insufficient user roles or privileges for the requested operation._

#### <a id="code-1102"></a>`1102` Session Expired  
User session or token has expired and must re-authenticate.  
_Probable cause: Token timeout or logout due to inactivity._

#### <a id="code-1200"></a>`1200` Invalid Input  
The input payload is malformed or contains invalid data.  
_Probable cause: Data format errors or invalid request parameters._

#### <a id="code-1201"></a>`1201` Missing Required Field  
A mandatory field is missing in the request payload.  
_Probable cause: Client omitted necessary data in the request._

#### <a id="code-1202"></a>`1202` Field Format Error  
One or more fields are incorrectly formatted or violate validation rules.  
_Probable cause: Validation failure due to incorrect data types or patterns._

#### <a id="code-1203"></a>`1203` Resource Not Found  
Requested resource does not exist or is inaccessible.  
_Probable cause: Invalid resource ID or resource has been deleted._

#### <a id="code-1204"></a>`1204` Request Conflict  
Request conflicts with current state of the resource, causing a conflict.  
_Probable cause: Duplicate resource creation or concurrent modification conflict._

#### <a id="code-1300"></a>`1300` Unknown Server Error  
An unexpected error occurred within the API server.  
_Probable cause: Unhandled exception or service failure._

#### <a id="code-1301"></a>`1301` External Service Unavailable  
Dependent external service is unreachable or down.  
_Probable cause: Network issues or third-party service downtime._

#### <a id="code-1302"></a>`1302` Timeout  
API request timed out waiting for a response or resource.  
_Probable cause: Slow external dependencies or heavy server load._

#### <a id="code-1303"></a>`1303` Configuration Error  
API configuration or environment settings are incorrect or missing.  
_Probable cause: Misconfigured environment variables or deployment errors._

---

### Database Codes

#### <a id="code-21100"></a>`21100` SQL Base Code  
General SQL database error without a specific cause.  
_Probable cause: Database connection failure or SQL execution error._

#### <a id="code-21101"></a>`21101` SQL Not Found  
Requested SQL record or resource was not found.  
_Probable cause: Query returned no results or invalid primary key._

#### <a id="code-21102"></a>`21102` SQL Connection Error  
Failed to connect to the SQL database.  
_Probable cause: Network issues, database server down, or credential problems._

#### <a id="code-21103"></a>`21103` SQL Resource Exists  
Attempted to create a resource that already exists in the database.  
_Probable cause: Violation of unique constraints or duplicate insert attempt._

#### <a id="code-21104"></a>`21104` SQL Resource Update Failed  
Update operation on SQL resource did not succeed.  
_Probable cause: Conflicting updates or constraint violations during update._

#### <a id="code-21105"></a>`21105` SQL Deletion Failed  
Failed to delete the specified SQL resource.  
_Probable cause: Foreign key constraints or resource not found._

#### <a id="code-21106"></a>`21106` SQL Record Update Exists  
Update operation conflicts with existing records.  
_Probable cause: Unique constraint violation or concurrent update conflict._

#### <a id="code-21107"></a>`21107` SQL Requested Delete Not Found  
Attempted to delete a SQL record that does not exist.  
_Probable cause: Invalid identifier or prior deletion._

#### <a id="code-21201"></a>`21201` SQL Integrity Error  
Integrity constraints (e.g., foreign key, unique) violated in SQL operation.  
_Probable cause: Inconsistent data or constraint violations._

#### <a id="code-21202"></a>`21202` SQL Data Error  
Invalid data encountered during SQL operation.  
_Probable cause: Data type mismatch or malformed input data._

#### <a id="code-21203"></a>`21203` SQL Operational Error  
SQL operation failed due to operational issues.  
_Probable cause: Database server overload, locked resources, or network issues._

#### <a id="code-21204"></a>`21204` SQL Programming Error  
Error in SQL syntax or incorrect database usage detected.  
_Probable cause: Bug in SQL query or incorrect database schema usage._

#### <a id="code-21205"></a>`21205` SQL Invalid Request  
Invalid or malformed SQL request.  
_Probable cause: Client sent invalid query or unsupported operation._

#### <a id="code-21205"></a>`21206` SQL Database Error  
It is a parent class of SQLAlchemy exceptions.   
If visible in logs there is some error that is uncaught.  
_Probable cause: Db session exception catching tree, uncaught sqlalchemy exception._


---

#### <a id="code-22100"></a>`22100` Mongo Base Code  
General MongoDB error without specific classification.  
_Probable cause: Connection failure or unexpected database exception._

#### <a id="code-22101"></a>`22101` Mongo Not Found  
MongoDB query returned no results for requested document.  
_Probable cause: Querying by non-existent ID or missing document._

#### <a id="code-22102"></a>`22102` Mongo Connection Error  
Failed to establish connection with MongoDB server.  
_Probable cause: Network issues, server downtime, or auth failure._

#### <a id="code-22103"></a>`22103` Mongo Resource Exists  
Attempted to insert a document that violates unique constraints.  
_Probable cause: Duplicate key error or existing document conflict._

#### <a id="code-22104"></a>`22104` Mongo Resource Update Failed  
Update operation on MongoDB document was unsuccessful.  
_Probable cause: Validation error or concurrency conflict._

#### <a id="code-22105"></a>`22105` Mongo Deletion Failed  
Failed to delete the specified MongoDB document.  
_Probable cause: Document not found or permission issues._

#### <a id="code-22106"></a>`22106` Mongo Record Update Exists  
Update conflicts with existing document constraints.  
_Probable cause: Duplicate key or concurrency violation._

#### <a id="code-22107"></a>`22107` Mongo Requested Delete Not Found  
Attempted deletion of a non-existent MongoDB document.  
_Probable cause: Document already deleted or invalid identifier._

#### <a id="code-22201"></a>`22201` Mongo Integrity Error  
Integrity constraint violation within MongoDB operation.  
_Probable cause: Data inconsistency or schema violation._

#### <a id="code-22202"></a>`22202` Mongo Data Error  
Invalid data detected during MongoDB processing.  
_Probable cause: Incorrect field types or malformed documents._

#### <a id="code-22203"></a>`22203` Mongo Operational Error  
MongoDB operation failed due to server or network issues.  
_Probable cause: Server overload, downtime, or connectivity problems._

#### <a id="code-22204"></a>`22204` Mongo Programming Error  
Programming or query error in MongoDB interaction.  
_Probable cause: Invalid query syntax or schema mismatch._

#### <a id="code-22205"></a>`22205` Mongo Invalid Request  
Malformed or unsupported MongoDB request.  
_Probable cause: Client sent invalid query or unsupported operation._

---

### Cloud Codes

#### <a id="code-31000"></a>`31000` Azure Base Error  
General Azure cloud service error with unspecified cause.  
_Probable cause: Azure service disruption or misconfiguration._

#### <a id="code-31001"></a>`31001` Azure Authentication Failure  
Failed to authenticate with Azure services.  
_Probable cause: Invalid credentials, expired tokens, or permission issues._

#### <a id="code-31002"></a>`31002` Azure Resource Not Available  
Requested Azure resource is unavailable or inaccessible.  
_Probable cause: Resource deleted, moved, or permissions revoked._

#### <a id="code-32000"></a>`32000` AWS Base Error  
Generic AWS cloud service error without detailed cause.  
_Probable cause: AWS service disruption or configuration errors._

#### <a id="code-32001"></a>`32001` AWS Permission Denied  
Access denied when performing AWS operation.  
_Probable cause: Insufficient IAM permissions or invalid credentials._

#### <a id="code-32002"></a>`32002` AWS Service Timeout  
AWS service request timed out waiting for response.  
_Probable cause: Network issues, high latency, or service overload._

#### <a id="code-33000"></a>`33000` GCP Base Error  
General Google Cloud Platform error without further details.  
_Probable cause: GCP service disruption or misconfiguration._

#### <a id="code-33001"></a>`33001` GCP Authentication Failure  
Failed authentication with GCP services.  
_Probable cause: Invalid service account keys or expired tokens._

#### <a id="code-33002"></a>`33002` GCP Quota Exceeded  
Exceeded GCP resource quotas or limits.  
_Probable cause: High usage exceeding allocated quotas._

---

### Reserved / Custom Codes

#### <a id="code-41101"></a>`41101` Promotion Expired  
Requested promotion or discount is no longer valid.  
_Probable cause: Promotion period ended or manually deactivated._

#### <a id="code-41102"></a>`41102` Payment Required  
Payment is required to proceed with the requested operation.  
_Probable cause: User account lacks valid payment or subscription._

#### <a id="code-41103"></a>`41103` Trial Limit Reached  
User has reached the maximum allowed trial usage or limits.  
_Probable cause: Trial period expired or usage exceeded allowed limits._
