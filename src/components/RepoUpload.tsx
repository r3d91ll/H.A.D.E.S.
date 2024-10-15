import React, { useState } from 'react';
import { Upload } from 'lucide-react';

const RepoUpload: React.FC = () => {
  const [repoUrl, setRepoUrl] = useState('');
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);
    setMessage('');

    try {
      const response = await fetch('/upload_repo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setMessage(data.message);
      setRepoUrl('');
    } catch (error) {
      setMessage('Error uploading repository');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="mt-6">
      <h2 className="text-lg font-semibold mb-2">Upload Git Repository</h2>
      <form onSubmit={handleUpload} className="flex items-center">
        <input
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="Enter Git repository URL"
          className="flex-grow mr-2 p-2 border border-gray-300 rounded"
        />
        <button
          type="submit"
          disabled={uploading}
          className={`bg-blue-500 text-white p-2 rounded flex items-center ${
            uploading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
          }`}
        >
          <Upload className="w-4 h-4 mr-2" />
          {uploading ? 'Uploading...' : 'Upload'}
        </button>
      </form>
      {message && <p className="mt-2 text-sm text-gray-600">{message}</p>}
    </div>
  );
};

export default RepoUpload;