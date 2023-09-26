"use client"

import { useState } from "react";


export default function Upload() {
  const BACKEND_URL = process.env.backend || "127.0.0.1";
  const FRONT = process.env.FRONT || "http";
  const PORT = process.env.PORT || "5000";

  const [output,setOutput] = useState(null)

  /**
   * Description placeholder
   * @date 9/27/2023 - 1:17:13 AM
   *
   * @param {React.MouseEvent<HTMLSpanElement, MouseEvent>}} event
   */
  const onFileChange = async (event) => {
    const file = event.target.files[0];

    const formdata = new FormData();
    formdata.append("file", file);

    const result  = await fetch(`${FRONT}://${BACKEND_URL}:${PORT}/api/upload`, {
      method: "POST",
      body: formdata,
    })

    setOutput('loading.........')

    const json = await result.json()

    console.log(json);
    setOutput(json.type)
  };

  // This function will open the native file browser dialog
  const openFileBrowser = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/jpeg,image/png";

    input.addEventListener("change", onFileChange);

    input.click();
  };

  return (
    <div className="custom-picture-selector">
      <span className="home-text11">
        <button onClick={openFileBrowser}>Select Picture</button>
        <b>result {output}</b>
        <br />
      </span>
    </div>
  );
}
