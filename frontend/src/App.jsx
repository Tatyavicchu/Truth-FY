import { useState } from 'react';
import Cookies from 'js-cookie';

function App() {
  const [link, setLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setResult(null); // Clear previous result
      const csrfToken = Cookies.get('csrftoken');
      const response = await fetch('https://your-backend-url/api/extract_text/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ link: link }),
      });
      const data = await response.json();
      console.log(data);

      if (data.prediction === 1) {
        setResult('This news article seems **FAKE** 🚨');
      } else if (data.prediction === 0) {
        setResult('This news article seems **REAL** ✅');
      } else {
        setResult('Could not determine the authenticity.');
      }
    } catch (error) {
      console.error('Error:', error);
      setResult('Something went wrong. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={{
        backgroundImage: 'url(/styling/image.jpeg)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        minHeight: '100vh',
        // color: 'white', // Adjust text color to stand out on the background
        padding: '20px'
      }}>
        <div className="flex justify-center items-center mt-10">
          <h1 className="font-extrabold text-6xl text-red-600">📰 TruthiFY</h1>
        </div>
        <div className="text-center my-10">
          <h1 className="text-3xl font-extrabold underline">Welcome to <span className="font-bold text-red-500 bg-black px-2">TruthiFY</span> – Your Trusted Fake News Checker!</h1>
          <p className="mt-4 text-xl font-bold text-">
            <span className='bg-white'>In today's fast-paced digital world, misinformation spreads like wildfire.</span> 
            <span className='bg-white'>TruthiFY is here to help you navigate the news landscape with confidence. </span>
            <span className='bg-white'>Our advanced AI model analyzes news articles and provides you with a quick </span>
            <span className='bg-white'>assessment of their authenticity. Just paste the link to the article, and <span className='bg-red-500 text-white'>let us do the rest!</span></span>
          </p>
        </div>

        <div className="flex justify-center items-center my-20 gap-4">
          <input
            id="link"
            type="text"
            placeholder="Enter the link here..."
            className="px-4 py-3 w-96 h-14 border-2 border-black rounded-lg text-xl"
            value={link}
            onChange={(e) => setLink(e.target.value)}
          />
          <button
            type="submit"
            onClick={handleSubmit}
            className="text-xl font-bold bg-red-500 hover:bg-red-600 text-white px-8 py-3 rounded-lg"
          >
            {loading ? 'Checking...' : 'Submit'}
          </button>
        </div>

        {loading && (
          <div className="flex justify-center items-center mt-10">
            <div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-20 w-20"></div>
          </div>
        )}

        {result && (
          <div className="flex justify-center items-center mt-10">
            <div className="text-2xl font-bold p-6 border-4 border-black rounded-lg">
              {result}
            </div>
          </div>
        )}

        {/* Add some quick styles for loader */}
        <style>{`
          .loader {
            border-top-color: #3498db;
            animation: spin 1s infinite linear;
          }
          @keyframes spin {
            to { transform: rotate(360deg); }
          }
        `}</style>
      </div>
    </>
  );
}

export default App;
