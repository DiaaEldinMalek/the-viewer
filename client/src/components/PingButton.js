import { useState } from 'react';

const PingButton = () => {
    const [pingResponse, setPingResponse] = useState(null);

    const testServer = async () => {
        try {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_BACKEND_API_BASE_URL}/ping`,
                {
                    method: 'GET',
                    headers: {
                        'ngrok-skip-browser-warning': 'true',
                    }
                }
            );

            if (response.ok) {
                setPingResponse("✓");
            } else {
                setPingResponse('Server error');
            }
        } catch (error) {
            setPingResponse('Failed to connect to server');
        }
    };

    return (<div className="test-server">

        <button onClick={testServer}>Ping Server </button>
        {<p>{pingResponse}</p>}
    </div>)
}

export default PingButton