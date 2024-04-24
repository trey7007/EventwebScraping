from jinja2 import Template
import json

class formatMessage:
    
    def  __init__(self):
        pass

    def createmessagetxt(self, events):
        html_text = """<!DOCTYPE html>
        <html>
        <body>
            <table style="width:100%">
                <!-- table header -->
                {% if events %}
                <tr>
                    {% for key in events[0] %}
                    <th> {{ key }} </th>
                    {% endfor %}
                </tr>
                {% endif %}

                <!-- table rows -->
                {% for dict_item in events %}
                <tr>
                    {% for value in dict_item.values() %}
                    <td> {{ value }} </td>
                    {% endfor %}
                </tr>
                {% endfor %}
                </table>
        </body>
        </html>"""


        my_templ = Template(html_text)
        
        with open('./Email/emailcontents.html', 'w') as f:
            f.write(my_templ.render(events=events))



msg = formatMessage()

with open("./FilteringEvents/filteredevents.json","r") as json_data:
    parsed_json = json.load(json_data)



msg.createmessagetxt(parsed_json)