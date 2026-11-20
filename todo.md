
# TODO
[~] fix functions that pass in unneccessary variables (eg. Board.Boardsize)
## lab 6 asyncio
- [x] wrap network communications in try/catch **********
    - [x] make sure return or pass as appropriate
    - [x] Server class
    - [x] run_server
    - [x] client
- [x] fix magic numbers **********
    - [x] Server class
    - [x] run_server
    - [x] client
- [x] add header comments **********
    - [x] Server class
    - [x] run_server
    - [x] client
- [x] fix windows naming bs w/ server.py
- [x] determine if self.server & related setters/getters needed (in Server class) - as written. could awkwardly wrap in () and use start forever, but 
then i think it may make it hard to close later if no variable for reference given not started directly in instance? look up later

    - [ ] Server.newclient() needs the tasks stored in self.variables or cleanup may remove them :/ then they need to be removed. but if i add refs to add client tasks to dictionary may break reads of it. need to scheck, no time

- [ ] make sure test code still passes
    - [ ] do we still need 100% coverage?
