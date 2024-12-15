import React from "react";

const Podium = ({ topSongs }) => {
  return (
    <div>


      <div className="flex justify-center items-end space-x-4 mt-10 mb-6">
        {/* Second Place */}
        {topSongs[1] && (
          <div className="flex flex-col items-center">
            <div className="bg-gray-300 text-black text-center w-52 h-56 rounded-md flex flex-col justify-center">
              <span className="font-bold text-xl">{topSongs[1].similarity.toFixed(2)}%</span>
              <span className="text-sm mt-2">{topSongs[1].metadata.title}</span>
            </div>
            <span className="text-lg mt-2">2nd</span>
          </div>
        )}
        {/* First Place */}
        {topSongs[0] && (
          <div className="flex flex-col items-center">
            <div className="bg-yellow-400 text-black text-center w-52 h-72 rounded-md flex flex-col justify-center">
              <span className="font-bold text-xl">{topSongs[0].similarity.toFixed(2)}%</span>
              <span className="text-sm mt-2">{topSongs[0].metadata.title}</span>
            </div>
            <span className="text-lg mt-2">1st</span>
          </div>
        )}
        {/* Third Place */}
        {topSongs[2] && (
          <div className="flex flex-col items-center">
            <div className="bg-gray-400 text-black text-center w-52 h-40 rounded-md flex flex-col justify-center">
              <span className="font-bold text-xl">{topSongs[2].similarity.toFixed(2)}%</span>
              <span className="text-sm mt-2">{topSongs[2].metadata.title}</span>
            </div>
            <span className="text-lg mt-2">3rd</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default Podium;
