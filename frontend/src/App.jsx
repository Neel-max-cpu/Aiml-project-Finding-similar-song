import React, { useState } from "react";
import SongSimilarity from "./components/SongSimilarity";
import Hero from "./components/Hero";

function App() {


  // test --
  /*
  const jsonStructure = {
    value: 1,
    left: {
      value: 2,
      left: {
        value: 4,
        left: {
          value: 8,
          left: null,
          right: null,
        },
        right: {
          value: 9,
          left: null,
          right: null,
        },
      },
      right: {
        value: 5,
        left: null,
        right: {
          value: 6,
          left: null,
          right: null,
        },
      },
    },
    right: {
      value: 7,
      left: {
        value: 3,
        left: {
          value: 10,
          left: {
            value: 12,
            left: null,
            right: {
              value: 13,
              left: null,
              right: null,
            },
          },
          right: null,
        },
        right: {
          value: 11,
          left: null,
          right: null,
        },
      },
      right: {
        value: 14,
        left: null,
        right: {
          value: 15,
          left: null,
          right: null,
        },
      },
    },
  };
  

  // function tree(node) {
  //   if (node == null) {
  //     return(
  //       <div className="border border-black rounded-full px-2 w-max">
  //         <h2>Null</h2>
  //       </div>        
  //     )
  //   }
  //   return (
  //     <>
  //       <div className="flex flex-col items-center">

  //         <div className="border border-black rounded-full px-2 w-max">
  //           {node.value}
  //         </div>         


        
  //         <div className="flex w-full justify-center">

  //           <div className="w-full">
  //             <div className="flex items-center justify-center">
  //               <h2>/</h2>
  //             </div>
  //             {tree(node.left)}
  //             </div>

  //           <div className='w-full'>
  //             <div className="flex items-center justify-center">
  //               <h2>\</h2>
  //             </div>
  //             {tree(node.right)}
  //           </div>

  //         </div>
  //       </div>

  //     </>

  //   )
  // }
  */

  return (   
    <div >
        {/* <SongSimilarity/> */}
        <Hero/>    
        {/* {tree(jsonStructure)} */}
    </div>       
  );
}

export default App;
