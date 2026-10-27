// ==========================================
// GET CURRENT USER
// ==========================================

function getCurrentUser() {

    return document
        .getElementById("currentUser")
        .value
        .trim();
}


// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {

    const sender = getCurrentUser();

    const receiver =
        document
            .getElementById("receiver")
            .value
            .trim();

    const messageBox =
        document.getElementById("messageInput");

    const message =
        messageBox.value.trim();


    if (!sender || !receiver || !message) {

        alert(
            "Please enter sender, receiver and message"
        );

        return;
    }


    try {

        const response = await fetch("/send", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                sender: sender,

                receiver: receiver,

                message: message

            })

        });


        const data = await response.json();


        if (response.ok) {

            alert(
                "Message Status: " +
                data.status
            );

            messageBox.value = "";

            loadMessages();

        }

        else {

            alert(
                "Error: " +
                (data.message || "Message not sent")
            );

        }

    }

    catch (error) {

        console.error(
            "SEND ERROR:",
            error
        );

        alert(
            "Server error. Check Flask."
        );

    }

}


// ==========================================
// LOAD MESSAGES
// ==========================================

async function loadMessages() {

    const currentUser =
        getCurrentUser();


    if (!currentUser) {

        return;
    }


    try {

        const response = await fetch(
            "/messages/" +
            encodeURIComponent(currentUser)
        );


        if (!response.ok) {

            console.error(
                "Message loading failed"
            );

            return;
        }


        const messages =
            await response.json();


        const chatBox =
            document.getElementById("chatBox");


        chatBox.innerHTML = "";


        messages.forEach(function (message) {

            // ==================================
            // MESSAGE DIV
            // ==================================

            const messageDiv =
                document.createElement("div");


            if (message.sender === currentUser) {

                messageDiv.className =
                    "message sent";

            }

            else {

                messageDiv.className =
                    "message received";

            }


            // ==================================
            // MESSAGE TEXT
            // ==================================

            const textDiv =
                document.createElement("span");

            textDiv.className =
                "message-text";

            textDiv.textContent =
                message.message;


            // ==================================
            // STATUS
            // ==================================

            const statusSpan =
                document.createElement("span");

            statusSpan.className =
                "message-status";


            // ==================================
            // SENDER STATUS
            // ==================================

            if (message.sender === currentUser) {


                if (message.status === "QUEUED") {

                    statusSpan.textContent = "✓";

                }


                else if (message.status === "SENT") {

                    statusSpan.textContent = "✓";

                }


                else if (
                    message.status === "DELIVERED"
                ) {

                    statusSpan.textContent = "✓✓";

                }


                else if (
                    message.status === "READ"
                ) {

                    statusSpan.textContent = "✓✓";

                    statusSpan.classList.add("read");

                }

            }


            // ==================================
            // ADD MESSAGE
            // ==================================

            messageDiv.appendChild(textDiv);

            messageDiv.appendChild(statusSpan);

            chatBox.appendChild(messageDiv);


            // ==================================
            // RECEIVER MESSAGE
            // MARK AS READ
            // ==================================

            if (
                message.receiver === currentUser &&
                message.status !== "READ"
            ) {

                markAsRead(message.id);

            }

        });


        // Scroll to bottom

        chatBox.scrollTop =
            chatBox.scrollHeight;


    }

    catch (error) {

        console.error(
            "LOAD ERROR:",
            error
        );

    }

}


// ==========================================
// MARK MESSAGE AS READ
// ==========================================

async function markAsRead(messageId) {

    if (!messageId) {

        console.error(
            "Message ID is missing"
        );

        return;
    }


    try {

        const response =
            await fetch(
                "/read/" +
                encodeURIComponent(messageId),
                {
                    method: "POST"
                }
            );


        const data =
            await response.json();


        console.log(
            "READ RESPONSE:",
            data
        );


        if (
            data.success &&
            data.status === "READ"
        ) {

            // Read successfully

            setTimeout(function () {

                loadMessages();

            }, 100);

        }

    }

    catch (error) {

        console.error(
            "READ ERROR:",
            error
        );

    }

}


// ==========================================
// AUTO REFRESH
// ==========================================

setInterval(function () {

    loadMessages();

}, 2000);


// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadMessages();

    }
);