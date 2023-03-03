<script>
    export let type;
    import axios from "axios";
    import { current_user_id } from "../store";
    export let alerts;

    let userID = $current_user_id;

    const get_timesheet_id = async (userID) => {
        let id;
        await axios
            .get(`http://0.0.0.0:8000/user/${userID}/timesheet`)
            .then((res) => (id = res.data));

        return id;
    };

    const clock_out = async () => {
        if (userID != 0) {
            let curr_time = Date.now();
            // This needs to be set to the current user - Global?

            try {
                let timesheet_id = await get_timesheet_id(userID);

                await axios
                    .patch(`http://0.0.0.0:8000/clock-out`, {
                        millis_out: curr_time,
                        timesheetID: timesheet_id,
                    })
                    .then(() =>
                        alerts.push(["Success", "Clocked out successfully!"])
                    );
                alerts = alerts;
            } catch (error) {
                alerts.push(["Error", error.response.data.detail]);
                alerts = alerts;
            }
            return;
        }
        alerts.push(["Error", "Please log in to clock out."]);
        alerts = alerts;
    };

    const clock_in = async () => {
        if (userID != 0) {
            let curr_time = Date.now();
            let timesheet_id = await get_timesheet_id(userID);

            try {
                await axios
                    .post(`http://0.0.0.0:8000/clock-in`, {
                        millis_in: curr_time,
                        timesheetID: timesheet_id,
                    })
                    .then(() =>
                        alerts.push(["Success", "Clocked in successfully!"])
                    );
                alerts = alerts;
            } catch (error) {
                alerts.push(["Error", error.response.data.detail]);
                alerts = alerts;
            }
            return;
        }
        alerts.push(["Error", "Please log in to clock in."]);
        alerts = alerts;
    };

    const triggerFunc = (type) => {
        if (type == "in") {
            clock_in();
        } else if (type == "out") {
            clock_out();
        }
    };
</script>

<div class="container">
    <div on:click={() => triggerFunc(type)} class="icon-container">
        {#if type == "in"}
            <div class="icon-in">
                <div class="hand minute minute-in" />
                <div class="hand hour in" />
                <div class="arrow-container arrow-in">
                    <div class="arrow left" />
                    <div class="arrow right" />
                </div>
                <div class="center" />
            </div>
        {:else if type == "out"}
            <div class="icon-out">
                <div class="hand minute minute-out" />
                <div class="hand hour out" />
                <div class="arrow-container arrow-out">
                    <div class="arrow top" />
                    <div class="arrow bottom" />
                </div>
                <div class="center" />
            </div>
        {/if}
    </div>
    <h1>
        {#if type == "in"}
            Clock In
        {:else}
            Clock Out
        {/if}
    </h1>
</div>

<style>
    .arrow-container {
        position: absolute;
        display: flex;
        height: 150px;
        width: 150px;
    }

    .arrow-in {
        align-items: flex-end;
        justify-content: center;
    }

    .arrow-out {
        align-items: center;
        justify-content: flex-end;
    }
    .arrow {
        position: absolute;
        opacity: 0;
        background: var(--primary);
        border-radius: 10px;
    }

    .top {
        width: 35px;
        height: 4px;
        transform: rotate(-45deg);
        margin-bottom: 15%;
    }

    .bottom {
        width: 35px;
        height: 4px;
        transform: rotate(45deg);
        margin-top: 15%;
    }

    .left {
        width: 4px;
        height: 35px;
        transform: rotate(-45deg);
        margin-right: 15%;
    }

    .right {
        width: 4px;
        height: 35px;
        transform: rotate(45deg);
        margin-left: 15%;
    }

    .container {
        display: flex;
        color: var(--text);
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .icon-container {
        cursor: pointer;
        display: flex;
        height: 200px;
        width: 200px;
        border-radius: 10%;
        background: var(--secondary);
        align-items: center;
        justify-content: center;
        border-style: solid;
        box-shadow: 10px 10px #333;
        transition: 0.5s;
    }

    .icon-container:active {
        box-shadow: 5px 5px #333;
        transform: translate(5px, 5px);
    }
    .icon-in,
    .icon-out {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 150px;
        width: 150px;
        border-radius: 50%;
        background: var(--text);
    }
    .hand {
        position: absolute;
        width: 4px;
        height: 60px;
        background-color: var(--primary);
        border-radius: 20%;
    }
    .minute {
        margin-bottom: 61px;
        transform-origin: 50% 100%;
    }
    .hour {
        height: 40px;
        /* width: 5px; */
    }

    .icon-container:hover .icon-out {
        animation: rotate-out 2s ease-in-out forwards;
    }

    .icon-container:hover .icon-in {
        animation: rotate-in 2s ease-in-out forwards;
    }

    .icon-container:hover .minute-out {
        animation: rotate-min-out 2s ease-in-out forwards;
    }

    .icon-container:hover .minute-in {
        animation: rotate-min-in 2s ease-in-out forwards;
    }

    .icon-container:hover .top {
        animation: fadein-top 2s ease-in-out forwards;
    }

    .icon-container:hover .bottom {
        animation: fadein-bottom 2s ease-in-out forwards;
    }

    .icon-container:hover .right {
        animation: fadein-top 2s ease-in-out forwards;
    }

    .icon-container:hover .left {
        animation: fadein-bottom 2s ease-in-out forwards;
    }

    .icon-container:hover .arrow-out {
        animation: correction-out 2s ease-in-out forwards;
    }

    .icon-container:hover .arrow-in {
        animation: correction-in 2s ease-in-out forwards;
    }

    .in {
        transform: rotate(-90deg);
        margin-left: -35px;
        transition: 0.5;
    }
    .out {
        transform: rotate(150deg);
        margin-top: 30px;
        margin-left: 18px;
    }

    .center {
        position: absolute;
        width: 6px;
        height: 6px;
        border-radius: 30%;
        background: var(--text);
    }

    @keyframes correction-out {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(60deg);
        }
        100% {
            transform: rotate(60deg);
        }
    }

    @keyframes correction-in {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(90deg);
        }
        100% {
            transform: rotate(90deg);
        }
    }

    @keyframes fadein-bottom {
        0% {
            transform: rotate(0);
            opacity: 0;
        }
        50% {
            transform: rotate(0);
            opacity: 0;
        }
        75% {
            transform: rotate(-45deg);
            opacity: 1;
        }
        100% {
            transform: rotate(-45deg);
            opacity: 1;
        }
    }

    @keyframes fadein-top {
        0% {
            transform: rotate(0);
            opacity: 0;
        }
        50% {
            transform: rotate(0);
            opacity: 0;
        }
        75% {
            transform: rotate(45deg);
            opacity: 1;
        }
        100% {
            transform: rotate(45deg);
            opacity: 1;
        }
    }

    @keyframes rotate-out {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(300deg);
        }
        100% {
            transform: rotate(300deg);
        }
    }

    @keyframes rotate-in {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(270deg);
        }
        100% {
            transform: rotate(270deg);
        }
    }

    @keyframes rotate-min-out {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(150deg);
        }
        100% {
            transform: rotate(150deg);
        }
    }

    @keyframes rotate-min-in {
        0% {
            transform: rotate(0);
        }
        50% {
            transform: rotate(270deg);
        }
        100% {
            transform: rotate(270deg);
        }
    }
</style>
