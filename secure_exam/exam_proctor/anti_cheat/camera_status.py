def camera_disabled(video_track):
    if not video_track:
        return True
    return video_track.readyState != "live"
