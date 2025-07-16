import requests
import json

def get_user_data(reddit_url):
    username = reddit_url.split('/')[-1]
    user_data = {
        'username': username,
        'posts': [],
        'comments': []
    }
    
    # Fetch user posts
    posts_url = f'https://www.reddit.com/user/{username}/submitted/.json'
    comments_url = f'https://www.reddit.com/user/{username}/comments/.json'
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Get posts
    response = requests.get(posts_url, headers=headers)
    if response.status_code == 200:
        posts = response.json()['data']['children']
        for post in posts:
            user_data['posts'].append({
                'title': post['data']['title'],
                'url': post['data']['url'],
                'subreddit': post['data']['subreddit'],
                'created_utc': post['data']['created_utc']
            })
    
    # Get comments
    response = requests.get(comments_url, headers=headers)
    if response.status_code == 200:
        comments = response.json()['data']['children']
        for comment in comments:
            user_data['comments'].append({
                'body': comment['data']['body'],
                'post_title': comment['data']['link_title'],
                'post_url': comment['data']['link_url'],
                'subreddit': comment['data']['subreddit'],
                'created_utc': comment['data']['created_utc']
            })
    
    return user_data

def build_user_persona(user_data):
    persona = {
        'username': user_data['username'],
        'interests': set(),
        'activity_summary': {
            'posts_count': len(user_data['posts']),
            'comments_count': len(user_data['comments']),
        },
        'citations': []
    }
    
    # Analyze posts and comments for interests
    for post in user_data['posts']:
        persona['interests'].add(post['subreddit'])
        persona['citations'].append(f"Post: {post['title']} - {post['url']}")
    
    for comment in user_data['comments']:
        persona['interests'].add(comment['subreddit'])
        persona['citations'].append(f"Comment on: {comment['post_title']} - {comment['post_url']}")
    
    persona['interests'] = list(persona['interests'])
    
    return persona

def save_persona_to_file(persona, filename='user_persona.txt'):
    with open(filename, 'w') as f:
        f.write(f"User Persona for {persona['username']}\n")
        f.write(f"Interests: {', '.join(persona['interests'])}\n")
        f.write(f"Activity Summary: {persona['activity_summary']}\n")
        f.write("Citations:\n")
        for citation in persona['citations']:
            f.write(f"- {citation}\n")

if __name__ == "__main__":
    reddit_url = input("Enter the Reddit user profile URL: ")
    user_data = get_user_data(reddit_url)
    user_persona = build_user_persona(user_data)
    save_persona_to_file(user_persona)
    print(f"User persona saved to user_persona.txt")
