<script>
    import axios from "axios";
    import DataTable from "../components/dataTable.svelte";

    let userTable = [];
    let teamTable = [];
    let timesheetTable = [];
    let entryTable = [];

    const get_users = async () => {
        userTable = [];
        await axios.get(`http://localhost:8000/user`).then((res) => {
            userTable = ["User"];
            for (let i = 0; i < res.data.length; i++) {
                userTable.push(res.data[i]);
            }
        });
    };

    const get_teams = async () => {
        teamTable = [];
        console.log(teamTable);
        await axios.get(`http://localhost:8000/team`).then((res) => {
            teamTable.push("Team");
            for (let i = 0; i < res.data.length; i++) {
                teamTable.push(res.data[i]);
            }
        });
    };

    const get_timesheet = async () => {
        timesheetTable = [];
        await axios.get(`http://localhost:8000/timesheet`).then((res) => {
            timesheetTable.push("Timesheet");
            for (let i = 0; i < res.data.length; i++) {
                timesheetTable.push(res.data[i]);
            }
        });
    };

    const get_entries = async () => {
        entryTable = [];
        await axios.get(`http://localhost:8000/entry`).then((res) => {
            entryTable.push("Entry");
            for (let i = 0; i < res.data.length; i++) {
                entryTable.push(res.data[i]);
            }
        });
    };
</script>

<div class="page">
    <div class="page-title">Database</div>

    <div class="tables">
        {#await get_teams() then _}
            <DataTable bind:data={teamTable} />
            <p>1-∞</p>
        {/await}
        {#await get_users() then _}
            <DataTable bind:data={userTable} />
            <p>1-1</p>
        {/await}
        {#await get_timesheet() then _}
            <DataTable bind:data={timesheetTable} />
            <p>1-∞</p>
        {/await}
        {#await get_entries() then _}
            <DataTable bind:data={entryTable} />
        {/await}
    </div>
</div>

<style>
    .tables {
        display: flex;
        flex-direction: row;
        width: 100%;
        align-items: center;
        margin-top: 20%;
    }

    p {
        color: var(--text);
        padding: 10px;
    }
</style>
