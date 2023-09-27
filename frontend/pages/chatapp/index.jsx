export default function ChatApp() {
    return <>
        <main className="chatapp">
            <h1>Chat App</h1>
            <div className="chatapp-container">
                <div className="chatapp-message">
                        <div className="chatapp-message-recived-sender">hi i am a chatbot</div>
                        <div className="chatapp-message-recived-client">hi</div>
                        <div className="chatapp-message-sending">sending</div>
                </div>
                <div className="chatapp-inputarea">
                    <input type="text" />
                </div>
            </div>
        </main>
        <style jsx>
            {`
            .chatapp-inputarea{
                border: 1px solid gray;
            }
            .chatapp{
                overflow: hidden;
            }
            .chatapp-message-recived-sender{
                displat: flex;
                flex-direciton: column;
            }
            main {
                display: flex;
                flex-direction: column;
                width: 100%;
                align-items: center;
                justify-content: center;
            }
            .chatapp-container{
                display: flex;
                flex-direction: column;
                max-width: 500px;
                width: 100%;
                height: 500px;
                border: 1px solid pink;
            }
            .chatapp-message{
                display: flex;
                flex-direction: column;
                height: 100%;
                justify-content: end;
                padding: 0 1rem 0 1rem;
                overflow-x: hidden;
                overlfow-y: scroll;
            }
            input{
                width: 100%;
                height: var(--dl-space-space-twounits);
            }
            .chatapp-message-recived-sender{
                display:flex;
                flex-direciton: column;
                width: 100%;
                height: var(--dl-space-space-twounits);
            }
            .chatapp-message-sending{
                display:flex;
                flex-direciton: column;
                width: 100%;
                height: var(--dl-space-space-twounits);
                justify-content: end;
            }
            .chatapp-message-recived-client{
                display:flex;
                flex-direciton: column;
                width: 100%;
                justify-content: end;
                height: var(--dl-space-space-twounits);
            }
        `}
        </style>
    </>
}