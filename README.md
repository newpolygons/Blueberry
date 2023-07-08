# Blueberry

 Currently Playing Spotify Song As Wallpaper for Gnome Desktop

 Once you stop the script, the wallpaper will be reset to the default one

## Images

![1](https://user-images.githubusercontent.com/30321729/145736816-33fa7ca4-7e9c-4299-9ea2-dbfe0acc78ab.png)

![2](https://user-images.githubusercontent.com/30321729/145736819-589ab479-38f9-4b61-9be9-61a02567dab4.png)

![3](https://user-images.githubusercontent.com/30321729/145736824-894d5452-89af-444f-b3f6-53925f9b4dce.png)

![4](https://user-images.githubusercontent.com/30321729/145736827-44439bc5-7ecc-4113-beda-442b0f210639.png)

![5](https://user-images.githubusercontent.com/30321729/145736829-f9a9aaed-2c9f-41aa-b490-2e77ee76b114.png)

## Usage

1. Download the repo
2. Run `pip install -r requirements.txt` in terminal to install dependencies
3. Start listening to music on Spotify
4. Create and fill 'creds.txt' in the main directory (more info below)
5. Run src/main.py file
6. Log in if web page comes up
7. Copy link of web page after signing in and paste into teminal
8. Enjoy!

### creds.txt

Create a file called 'creds.txt' in the main directory and fill it with the following:

``` txt
client_id = your_client_id
client_secret = your_client_secret
spot_username = your_spotify_username
display_size = your_display_size (ex. 1920x1080)
```

### How to get client_id and client_secret

1. Go to <https://developer.spotify.com/dashboard/applications>
2. Log in with your Spotify account
3. Select 'Create an app'
4. Choose a name and description for your app, then click 'Create'
5. Click con 'Edit Settings' and set '<https://google.com/>' as new redirect URI, then Save
6. In the app page, copy the Client ID and Client Secret and paste them in the 'creds.txt' file
7. Write your Spotify username in the 'creds.txt' file
8. Copy your display size (ex. 1920x1080) and paste it in the 'creds.txt' file (you can find it in Settings -> Devices -> Display Resolution or running the command `xrandr` in terminal)
9. Save the file
