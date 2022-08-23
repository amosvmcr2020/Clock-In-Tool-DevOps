<script>
    export let type;
    import axios from "axios";
    export let response;

    const get_timesheet_id = async (userID) => {
        let id;
        await axios
            .get(`http://localhost:8000/user/${userID}/timesheet`)
            .then((res) => (id = res.data));

        return id;
    };

    const clock_out = async () => {
        let curr_time = Date.now();
        // This needs to be set to the current user - Global?
        let userID = 2;

        try {
            let timesheet_id = await get_timesheet_id(userID);

            await axios
                .put(`http://localhost:8000/clock-out`, {
                    millis_out: curr_time,
                    timesheetID: timesheet_id,
                })
                .then((res) => (response = res.data));
        } catch (error) {
            response = error.response.data.detail;
        }
    };

    const clock_in = async () => {
        let curr_time = Date.now();
        // This needs to be set to the current user - Global?
        let userID = 2;

        let timesheet_id = await get_timesheet_id(userID);

        try {
            await axios
                .post(`http://localhost:8000/clock-in`, {
                    millis_in: curr_time,
                    timesheetID: timesheet_id,
                })
                .then((res) => (response = res.data));
        } catch (error) {
            response = error.response.data.detail;
        }
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
        <div class="icon">
            <div class="hand minute" />
            {#if type == "in"}
                <div class="hand hour in" />
            {:else if type == "out"}
                <div class="hand hour out" />
            {/if}
            <div class="center" />
        </div>
        <div class="arrow top" />
        <div class="arrow bottom" />
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
    .arrow {
        position: absolute;
        width: 4px;
        height: 30px;
        background: red;
    }
    .top {
        transform: translate(500%, 10%);
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
    }

    .icon-container:active {
        box-shadow: 5px 5px #333;
        transform: translate(5px, 5px);
    }
    .icon {
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
        margin-bottom: 55px;
        transform-origin: 50% 100%;
    }
    .hour {
        height: 40px;
        width: 5px;
    }

    .icon-container:hover .icon {
        animation: rotate 1s ease-in-out forwards;
    }

    .icon-container:hover .minute {
        animation: rotate-min 1s ease-in-out forwards;
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

    @keyframes rotate {
        0% {
            transform: rotate(0);
        }
        100% {
            transform: rotate(300deg);
        }
    }

    @keyframes rotate-min {
        0% {
            transform: rotate(0);
        }
        100% {
            transform: rotate(150deg);
        }
    }
</style>
