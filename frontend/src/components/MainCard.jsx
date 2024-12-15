import React from 'react'
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "./ui/card"

const MainCard = ({song, index}) => {
    return (
        <div className='shadow-xl'>
            <Card key={index} className=''>
                <CardHeader>
                    <CardTitle>
                        Title: {song.metadata.title}
                    </CardTitle>
                    <CardDescription>
                        Artist: {song.metadata.artist_name}
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <p>Album: {song.metadata.album_name}</p>
                    <p>{song.metadata.year}</p>
                    <p>Similarity: {song.similarity === 0 ? "Very Low" : song.similarity.toFixed(2) + "%"}</p>
                </CardContent>
            </Card>
        </div>
    )
}

export default MainCard
