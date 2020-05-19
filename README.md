# This is my Dashboard for COVID-19 stats/data

##### Also my first attempt at front-end
<a href = "https://covid-19-website-daily.herokuapp.com/">My Current working deployment </a>
<br>May 16:<br>
<p>Note: Always add <code>gunicorn</code> in the requirements.txt </p>
<br>May 17:<br>
<p>The app takes almost 23 seconds to execute, looking for alternate method to keep data ready</p>
<br>May 18:<br>
<p><code>from apscheduler.schedulers.background import BackgroundScheduler</code><br>
The above has helped me achieve what I was looking for. Since update the retrieve time has drastically 
come down to 1 second response from server</p><br><p>Note: <code>render_template</code> has to be inside any app.route<br>
Even though reponse time is lower, the app goes into idling until dyno is started. Looking for a way around that</p>
<br>
<br>May 19:<br>
<p>
<ul>
    <li>Added color value on top of bars for better understanding of data</li>
    <li>Hits self to stay awake</li>
    <li>Added Logger</li> 
</ul></p>
