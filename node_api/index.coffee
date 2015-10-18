# Import Modules
express = require 'express'
request = require 'request'
mysql = require 'mysql'
bodyParser = require 'body-parser'
_ = require 'lodash'

app = express()

app.set('port', (process.env.PORT || 5000))
app.use(express.static(__dirname + '/public'))
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended: true}))

# Connect MySQL
db_connection = mysql.createPool
  host: process.env.DB_HOST || 'localhost',
  user: process.env.DB_USER || 'test_user',
  password: process.env.DB_PASS || 'test_password',
  database: process.env.DB_NAME || 'test_db'

# Jubatus API Endpoint
JUBATUS_RECOMMEND_API = 'http://127.0.0.1:8030/api/recommender'

# Cross-domain authorization
app.all '/*', (request, response, next) ->
    response.contentType 'json'
    response.header 'Access-Control-Allow-Origin', '*'
    do next


app.get '/', (req,res) ->
  res.send 'RecommenderAPI'


# Request Recent Posts
app.get '/posts', (req,res) ->

  # Measuring the processing time
  startTime = new Date()

  # Query
  db_connection.query '
    SELECT *
    FROM posts
    WHERE created > (NOW() - INTERVAL 5 DAY)
    ORDER BY RAND()
    LIMIT 20
    '
    , (err, rows) ->

      # Error Check
      if err
        console.log err

      # Calculate the processing time
      endTime = new Date()
      processing_time = endTime - startTime
      console.log processing_time + "ms"

      # Shaping the response data
      res_data =
        processing_time : processing_time
        data : rows

      # Return data
      res.send res_data


# Request Post Recommends
app.get '/recommender', (req,res) ->

  # Measuring the processing time
  startTime = new Date()

  # Check Query
  if req.query.title
    req_title = encodeURIComponent(req.query.title)

  # Jubatus Request
  request "#{JUBATUS_RECOMMEND_API}?textdata=#{req_title}", (error, response, body) ->

      # Success to get Recommend PostIds from Jubatus
      if (!error && response.statusCode == 200)
        postIds = JSON.parse(body).map (row)-> row.posts_id

        # Get Posts MainData from MySQL
        db_connection.query "SELECT * FROM posts WHERE id IN (#{postIds})", (err, rows) ->

          # Check Error
          if err
            console.log err

          # Calculate the processing time
          endTime = new Date()
          processing_time = endTime - startTime
          console.log processing_time + "ms"

          # Shaping the response data
          res_data =
            processing_time : processing_time
            data : rows

          # Return data
          res.send res_data


# Listen
app.listen app.get('port'), ->
  console.log "Node app is running at localhost:#{app.get('port')}"
