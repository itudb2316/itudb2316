CREATE TABLE teamshalf_teams(
  teamID varchar(3) NOT NULL,
  lgID varchar(2) DEFAULT NULL,
  divID varchar(1) DEFAULT NULL,
  name varchar(50) DEFAULT NULL,
  PRIMARY KEY (`teamID`)
);



INSERT INTO teamshalf_teams (teamID, lgID, divID, name) VALUES
('ATL', 'NL', 'W', 'Atlanta Braves'),
('BAL', 'AL', 'E', 'Baltimore Orioles'),
('BOS', 'AL', 'E', 'Boston Red Socks'),
('CAL', 'AL', 'W', 'California Angels'),
('CHA', 'AL', 'W', 'Chicago White Socks'),
('CHN', 'NL', 'E', 'Chicago Cubs'),
('CIN', 'NL', 'W', 'Cincinnati Reds'),
('CLE', 'AL', 'E', 'Cleveland Indians'),
('DET', 'AL', 'E', 'Detroit Tigers'),
('HOU', 'NL', 'W', 'Houston Astros'),
('KCA', 'AL', 'W', 'Kansas City Royals'),
('LAN', 'NL', 'W', 'Los Angeles Dodgers'),
('MIN', 'AL', 'W', 'Minnesota Twins'),
('ML4', 'AL', 'E', 'Milwaukee Brewers'),
('MON', 'NL', 'E', 'Montreal Expos'),
('NYA', 'AL', 'E', 'New York Yankees'),
('NYN', 'NL', 'E', 'New York Mets'),
('OAK', 'AL', 'W', 'Oakland Athletics'),
('PHI', 'NL', 'E', 'Philadelphia Phillies'),
('PIT', 'NL', 'E', 'Pittsburgh Pirates'),
('SDN', 'NL', 'W', 'San Diego Padres'),
('SEA', 'AL', 'W', 'Seattle Mariners'),
('SFN', 'NL', 'W', 'San Francisco Giants'),
('SLN', 'NL', 'E', 'St. Louis Cardinals'),
('TEX', 'AL', 'W', 'Texas Rangers'),
('TOR', 'AL', 'E', 'Toronto Blue Jays');



ALTER TABLE teamshalf DROP COLUMN lgID;



ALTER TABLE teamshalf DROP COLUMN divID;
