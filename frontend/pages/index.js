import React, { useEffect, useState} from 'react'
import Head from 'next/head'
import  Upload  from '../component/Upload'

const Home = (props) => {
  return (
    <>
      <div className={'home-container'}>
        <Head>
          <title>NOidea</title>
          <meta property="og:title" content="NOidea" />
        </Head>
        <main className="home-about">
          <div className="home-container1">
            <h1 className="home-text07">
              <span>
                I inadvertently went to See&apos;s Candy last week (I was in the
                mall looking for phone repair), and as it turns out, See&apos;s
                Candy now charges a dollar
              </span>
              <br></br>
            </h1>
            <span className="home-text10">
              The piano sat silently in the corner of the room. Nobody could
              remember the last time it had been played. The little girl walked
              up to it and hit a few of the keys. The sound of the piano rang
              throughout the house for the first time in years. In the upstairs
              room, confined to her bed, the owner of the house had tears in her
              eyes
            </span>
          </div>
          <div className="home-container2">
            <img
              alt="image"
              src="/pexels-antoni-shkraba-5214949-removebg-preview-600h.png"
              className="home-image1"
            />
          </div>
        </main>
        <div className="home-chat-bot">
          <Upload />
        </div>
      </div>
    </>
  )
}


export default Home
