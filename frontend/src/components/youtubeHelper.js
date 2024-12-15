import axios from 'axios';

export const getYouTubeLink = async (title, artist) => {
    const apiKey = import.meta.env.VITE_API_KEY;
    const query = `${title} ${artist}`;
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&key=${apiKey}`;

    try {
        const response = await axios.get(url);
        const videoId = response.data.items[0]?.id?.videoId;

        // Return YouTube URL if a video is found
        if (videoId) {
            return `https://www.youtube.com/watch?v=${videoId}`;
        } else {
            return null;
        }
    } catch (error) {
        console.error('Error fetching YouTube link:', error);
        return null;
    }
};
