# Lab1 - OpenAPI

### Tasks
- plan and understand the appplication
- write a YAML file used for furthre labs

### Purpose
This application gathers user login activity and performance from League of Legends API. This data will be processed and displayed on a dashboard for users to analyze their own and others' performances. 

### Event 1 - User Activity
The receiver service will gather user activity cosisting of `user_id`, `region`, `login_counts` and `timestamp`.

### Event 2 - Performance
The receiver service will gather user permforance in a match consisting of `match_id`, `user_id`, `kill`, `death`, `assist` and `timestamp`. 

### Peak Events
These two events surge significantly on Friday and Saturday nights when students finish school. We anticipate a peak activity rate of 5,000 players logging in per second and 10,000 matches starting per second.

### Types of User
- **Players**
  - Access their in-game performance
- **Game developers**
  - Track whether champions are balanced
  - Analyze whether two teams are matched in skill
- **Streamers**
  - Schedule streams based on user activity

