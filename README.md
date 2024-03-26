\*\*\* Python INSTRUCTIONS

- Run file
  `Python3 main.py`

\*\*\* DOCKER INSTRUCTIONS

- BUILD IMAGE
  `docker build . -t get-logs`

- RUN CONTAINER with env file

  - command: `docker run -v <host file path dir>:/app/logs --env-file .env get-logs`
  - example: `docker run -v /Users/paul/Documents/Python/logs:/app/logs --env-file .env get-logs`
  - an .env file is required for this to work

- RUN CONTAINER with env arguements

  - command: `docker run -v <host file path dir>:/app/logs -e path=<path> -e hostname=<hostname> -e username=<username> -e password=<password> get-logs`
  - example: `docker run -v /Users/Spiderman/Documents/Python/logs:/app/logs -e path='my_logs' -e hostname='ftp.somewhere.net' -e username='user001' -e password='password123' get-logs`
  - an .env file is required for this to work
