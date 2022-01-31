#!/usr/bin/env python
import json
import sys
from datetime import datetime
from string import Template

if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} [data/dir] [output/dir]')
    sys.exit(0)

summary_template = Template("""
$summary
<p>JEP: <a href="$full_jep_link">$full_jep_link</a></p>
<p>ISSUE: <a href="$issue">$issue</a></p>
""")

def process_date(date_str):
    dt = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return {'year': dt.year, 'month': dt.month, 'day': dt.day}

def find_jep(jep_data, jep_id):
    return next((x for x in jep_data if x['id'] == jep_id), None)

def create_event_from_jep(jep):
    start_date = process_date(jep['created'])
    summary = summary_template.substitute(summary=jep['summary'], full_jep_link=jep['full_jep_link'], issue=jep['issue'])
    text = {'headline': f'{jep["id"]}: {jep["title"]}', 'text': summary}
    return {'start_date': start_date, 'text': text}

def create_event_from_jdk(jdk):
    if 'release_date' in jdk and jdk['release_date'] != '(in development)':
        dt = datetime.strptime(jdk['release_date'], 'GA %Y/%m/%d')
        start_date = {'year': dt.year, 'month': dt.month, 'day': dt.day}
        summary = jdk['summary']
        text = {'headline': f'JDK {jdk["version"]}', 'text': summary}
        return {'start_date': start_date, 'text': text}
    else:
        return None

data_dir = sys.argv[1]
jep_data = json.load(open(f'{data_dir}/scraped-jeps.json'))
jdk_data = json.load(open(f'{data_dir}/scraped-jdks.json'))
output_dir = sys.argv[2]

jdk_events = []

for jdk in jdk_data:
    events = []

    title_text = {'headline': f'JDK{jdk["version"]}', 'text': jdk['summary']}
    title = {'text': title_text}

    newdata = {'events': events, 'title': title}

    for jep_id in jdk['jeps']:
        jep = find_jep(jep_data, jep_id)
        event = create_event_from_jep(jep)
        events.append(event)

    jdk_event = create_event_from_jdk(jdk)
    if jdk_event is not None:
        jdk_events.append(jdk_event)

    with open(f'{output_dir}/{jdk["version"]}.json', 'w') as f:
        f.write(json.dumps(newdata))

with open(f'{output_dir}/jdks.json', 'w') as f:
    f.write(json.dumps({'events': jdk_events}))

for jep in jep_data:
    event = create_event_from_jep(jep)
    with open(f'{output_dir}/{jep["id"]}.json', 'w') as f:
        f.write(json.dumps(event))

"""
The data file should be in JSON format with the following structure
{
    "events": [
        {
            "start_date": {
                "year":         "1900",
                "month":        "01",
                "day":          "05",
                "hour":         "",
                "minute":       "",
                "second":       "",
                "millisecond":  "",
                "format":       ""
            },
            "end_date": {
                "year":         "1900",
                "month":        "06",
                "day":          "07",
                "hour":         "",
                "minute":       "",
                "second":       "",
                "millisecond":  "",
                "format":       ""
            },
            "media": {
                "caption":  "",
                "credit":   "",
                "url":      "url_to_your_media.jpg",
                "thumbnail":    "url_to_your_media.jpg"
            },
            "text": {
                "headline": "Headline Goes Here",
                "text":     "Your slide text goes here."
            }
        }
    ]
}
"""
