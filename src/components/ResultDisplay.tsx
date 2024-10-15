import React from 'react';

interface ResultDisplayProps {
  result: string;
  loading: boolean;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, loading }) => {
  if (loading) {
    return <div className="text-center text-gray-600">Processing your query...</div>;
  }

  if (!result) {
    return null;
  }

  const lines = result.split('\n');

  return (
    <div className="bg-gray-100 p-4 rounded-lg">
      <h2 className="text-xl font-semibold mb-2">Result:</h2>
      <div className="whitespace-pre-wrap text-sm">
        {lines.map((line, index) => {
          if (line.startsWith('Thought:')) {
            return <p key={index} className="text-blue-600">{line}</p>;
          } else if (line.startsWith('Action:')) {
            return <p key={index} className="text-green-600">{line}</p>;
          } else if (line.startsWith('Observation:')) {
            return <p key={index} className="text-orange-600">{line}</p>;
          } else if (line.startsWith('Answer:')) {
            return <p key={index} className="text-purple-600 font-bold">{line}</p>;
          } else {
            return <p key={index}>{line}</p>;
          }
        })}
      </div>
    </div>
  );
};

export default ResultDisplay;