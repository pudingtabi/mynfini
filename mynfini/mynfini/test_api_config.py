from config import Config

c = Config()
print('API Key Configured:', c.API_KEY != 'your-api-key-here')
print('Secret Key Source:', 'Environment' if 'SECRET_KEY' in __import__('os').environ else 'Default')
print('Current API Key:', c.API_KEY[:10] + '...' if len(c.API_KEY) > 10 else 'Too short')