import React, { useEffect, useState } from 'react'
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./ui/card"

import { getYouTubeLink } from './youtubeHelper';

const MainCard = ({ song, index }) => {
    const [youtubeLink, setYouTubeLink] = useState(null);

    useEffect(() => {
        // Fetch YouTube link when component mounts
        const fetchYouTubeLink = async () => {
            const link = await getYouTubeLink(song.metadata.title, song.metadata.artist_name);
            setYouTubeLink(link);
        };

        fetchYouTubeLink();
    }, [song]);

    return (
        <div className='shadow-xl'>
            <Card key={index} className=''>
                <CardHeader>
                    <CardTitle>
                        #{index+1}
                    </CardTitle>
                    <CardTitle>
                        Song: {song.metadata.title}
                    </CardTitle>
                    <CardDescription>
                        Artist: {song.metadata.artist_name}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    {/* Conditionally render the YouTube link if available */}
                    {youtubeLink && (
                        <p>
                            <a
                                href={youtubeLink}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-blue-600 hover:underline"
                            >
                                Watch on YouTube
                            </a>
                        </p>
                    )}
                    <p>Album: {song.metadata.album_name}</p>
                    <p>Year: {song.metadata.year}</p>
                    <p>Similarity: {song.similarity === 0 ? "Very Low" : song.similarity.toFixed(2) + "%"}</p>
                </CardContent>
            </Card>
        </div>
    )
}

export default MainCard
