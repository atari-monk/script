# Balanced settings
# ffmpeg -f gdigrab -framerate 30 -thread_queue_size 1024 -i desktop -f dshow -thread_queue_size 1024 -i audio="Miks stereo (Realtek(R) Audio)" -c:v # libx264 -preset veryfast -crf 15 -pix_fmt yuv420p -c:a aac output.mkv

# Maximum quality for screen recording
ffmpeg -f gdigrab -framerate 30 -thread_queue_size 1024 -i desktop -f dshow -thread_queue_size 1024 -i audio="Miks stereo (Realtek(R) Audio)" -c:v libx264 -preset faster -crf 12 -pix_fmt yuv420p -profile:v high -level 4.1 -c:a aac -b:a 192k output.mkv