import json
import boto3
import uuid
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

# Patch all supported libraries for X-Ray
patch_all()

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('<Your-DynamoDB-TableName>')

def lambda_handler(event, context):
    try:
        # Determine the HTTP method and path
        http_method = event['httpMethod']
        path = event['path']

        # Add annotations for the request (Lambda level)
        with xray_recorder.in_subsegment('Lambda_Annotation') as subsegment:
            subsegment.put_annotation('http_method', http_method)
            subsegment.put_annotation('path', path)
        print(f"Request received: {http_method} {path}")  # Debugging

        if http_method == 'GET' and path == '/ui': #Replace with appropriate API gateway PATH if necessary
            # Generate the API Gateway URL dynamically
            api_url = f"https://{event['requestContext']['domainName']}/{event['requestContext']['stage']}"
            
            html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <title>To-Do List</title>
              <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                #todo-list {{ margin-top: 20px; }}
                .todo-item {{ padding: 10px; border: 1px solid #ccc; margin-bottom: 10px; border-radius: 5px; }}
                #add-todo-form {{ margin-top: 20px; }}
                input[type="text"] {{ padding: 8px; width: 200px; margin-right: 10px; }}
                button {{ padding: 8px 12px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; }}
                button:hover {{ background-color: #218838; }}
              </style>
            </head>
            <body>
              <h1>To-Do List</h1>

              <!-- Display To-Do List -->
              <div id="todo-list">
                <h2>Your To-Dos</h2>
                <div id="todos"></div>
              </div>

              <!-- Add New To-Do Form -->
              <div id="add-todo-form">
                <h2>Add a New To-Do</h2>
                <input type="text" id="todo-title" placeholder="Enter a to-do title">
                <button onclick="addTodo()">Add To-Do</button>
              </div>

              <script>
                const apiUrl = '{api_url}';

                // Fetch and display todos
                async function fetchTodos() {{
                  try {{
                    const response = await fetch(apiUrl + '/todos');
                    const data = await response.json();

                    if (!Array.isArray(data.todos)) {{
                      console.error("Invalid response format:", data);
                      return;
                    }}

                    const todosContainer = document.getElementById('todos');
                    todosContainer.innerHTML = '';

                    data.todos.forEach(todo => {{
                      const todoItem = document.createElement('div');
                      todoItem.className = 'todo-item';
                      todoItem.innerHTML = `
                        <strong>${{todo.title}}</strong> (Status: ${{todo.status}})
                      `;
                      todosContainer.appendChild(todoItem);
                    }}); 
                  }} catch (error) {{
                    console.error('Error fetching todos:', error);
                  }}
                }}

                // Add a new todo
                async function addTodo() {{
                  const title = document.getElementById('todo-title').value;
                  if (!title) {{
                    alert('Please enter a to-do title.');
                    return;
                  }}

                  try {{
                    const response = await fetch(apiUrl + '/todos', {{
                      method: 'POST',
                      headers: {{ 'Content-Type': 'application/json' }} ,
                      body: JSON.stringify({{ title, status: 'pending' }}),
                    }});

                    if (response.ok) {{
                      document.getElementById('todo-title').value = ''; // Clear input
                      fetchTodos(); // Refresh the to-do list
                    }} else {{
                      console.error('Error adding todo:', response.statusText);
                    }}
                  }} catch (error) {{
                    console.error('Error adding todo:', error);
                  }}
                }}

                // Load todos when the page loads
                fetchTodos();
              </script>
            </body>
            </html>
            """
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': html,
            }

        elif http_method == 'GET' and path == '/todos': #Replace with appropriate API gateway PATH if necessary
            # DynamoDB scan operation with annotations
            with xray_recorder.in_subsegment('DynamoDB_GetTodos') as subsegment:
                try:
                    response = table.scan()
                    todos = response.get('Items', [])
                    subsegment.put_metadata('todos', todos)  # Add metadata for fetched todos
                    print(f"Fetched todos: {todos}")  # Debugging
                except Exception as e:
                    subsegment.put_annotation('error', str(e))  # Add annotation for errors
                    print(f"DynamoDB error: {e}")  # Debugging
                    raise e

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({'todos': todos}),
            }

        elif http_method == 'POST' and path == '/todos': #Replace with appropriate API gateway PATH if necessary
            # Parse the request body and DynamoDB put_item operation with annotations
            body = json.loads(event['body'])
            todo_id = str(uuid.uuid4())
            title = body['title']
            status = body.get('status', 'pending')

            with xray_recorder.in_subsegment('DynamoDB_PutTodo') as subsegment:
                try:
                    table.put_item(Item={
                        'id': todo_id,
                        'title': title,
                        'status': status,
                    })
                    subsegment.put_metadata('todo_item', {'id': todo_id, 'title': title, 'status': status})  # Add metadata for the new todo
                    print(f"Added todo: {title}")  # Debugging
                except Exception as e:
                    subsegment.put_annotation('error', str(e))  # Add annotation for errors
                    print(f"DynamoDB error during PUT: {e}")  # Debugging
                    raise e

            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                },
                'body': json.dumps({'id': todo_id, 'title': title, 'status': status}),
            }

        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Not Found'}),
            }

    except Exception as e:
        # Add error annotation to the Lambda segment
        with xray_recorder.in_subsegment('Lambda_Error') as subsegment:
            subsegment.put_annotation('error', str(e))
        print(f"Lambda error: {e}")  # Debugging
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}),
        }

