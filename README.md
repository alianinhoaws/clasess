# Server OOP
Web server, store data into DB
binded port 8080

URLs:
/companies
/users

Available methods:
- GET
- POST
- PUT
- DELETE

Mandatory args.
for user:
- name: 'Name'
- surname: 'Surname'
- birthday: '22/08/2010'
- telephone: '0671230213'

for companies:
- name: 'Name'
- address: 'Address'
- telephone: '0671230213'

Examples:
* curl -X POST  -d name='CompanyX' -d address='London' -d telephone='0685930245' localhost:8080/companies/
* curl -X PUT  -d name='CoOSTanyX' -d address='London' -d telephone='0685930245' localhost:8080/companies/22
* curl -X DELETE localhost:8080/companies/1
* curl -X GET localhost:8080/companies/[id] id optional, without returns all data from DB per entity 
