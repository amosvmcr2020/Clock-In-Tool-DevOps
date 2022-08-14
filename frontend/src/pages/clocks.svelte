<script>
    import axios from "axios";
    let response;

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
        let userID = 3;

        let timesheet_id = await get_timesheet_id(userID);

        await axios
            .put(`http://localhost:8000/clock-out`, {
                millis_out: curr_time,
                timesheetID: timesheet_id,
            })
            .then((res) => (response = res.data));
    };

    const clock_in = async () => {
        let curr_time = Date.now();
        // This needs to be set to the current user - Global?
        let userID = 3;

        let timesheet_id = await get_timesheet_id(userID);

        await axios
            .post(`http://localhost:8000/clock-in`, {
                millis_in: curr_time,
                timesheetID: timesheet_id,
            })
            .then((res) => (response = res.data));
    };
</script>

<div class="page">
    <div class="page-title">Log your time</div>
    <div class="content-container">
        <div class="container-title">Clock in/out</div>
        <div class="content">
            <button on:click={() => clock_in()}>Clock In</button>
            <button on:click={() => clock_out()}>Clock Out</button>
        </div>
        {#if response}
            <div class="content">
                <p>{response}</p>
            </div>
        {/if}
    </div>
</div>
