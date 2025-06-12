RELEASES

- Release 1.0.0: Download all default_docker logs
- Release 2.0.0: Download and merge log files by date
- Release 3.0.0: Supports multiple instances
- Release 4.0.0: Supports multiple slots / ftp servers

\*\*\* ENV STRUCTURE

- `hostname=[ftp server]`
- `username=]ftp username`
- `password=[ftp password]`

- if you're using multiple hostnames/usernames/passwords then seperate with a semicolon ;

\*\*\* PYTHON INSTRUCTIONS

- Run file with env file
  `Python3 main.py`

\*\*\* DOCKER INSTRUCTIONS

- BUILD IMAGE
  `docker build . -t get-logs`

- RUN CONTAINER with env file

  - command: `docker run -v <host file path dir>:/app/logs --env-file .env get-logs`
  - example: `docker run -v /Users/Groot/Documents/Python/logs:/app/logs --env-file .env get-logs`
  - an .env file is required for this to work

- RUN CONTAINER with env arguements

  - command: `docker run -v <host file path dir>:/app/logs -e path=<path> -e hostname=<hostname> -e username=<username> -e password=<password> get-logs`
  - example: `docker run -v /Users/Groot/Documents/Python/logs:/app/logs -e path='my_logs' -e hostname='ftp.somewhere.net' -e username='user001' -e password='password123' get-logs`
  - an .env file is required for this to work
