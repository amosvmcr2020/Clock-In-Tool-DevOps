<script>
    import axios from "axios";

    let user;
    let times = [];

    const get_timesheet = async (user_id) => {
        await axios
            .get(`http://localhost:8000/user/${user_id}/timesheet/summary`)
            .then((res) => (times = res.data.times));
        return times;
    };

    const get_current_user = async () => {
        await axios
            .get(`http://localhost:8000/user`)
            .then((res) => (user = res.data[1]));
        return user;
    };

    // const get_current_user = async () => {
    //     await axios
    //         .get(`http://localhost:8000/user/${user_id}`)
    //         .then((res) => (user = res.data));
    //     return user;
    // };

    const translate_date = (date_str) => {
        let date = new Date(date_str);
        date = date.toLocaleTimeString();
        return date;
    };
</script>

<div class="page">
    {#await get_current_user()}
        Loading
    {:then user}
        <div class="page-title">Hello {user.username}!</div>
        {#await get_timesheet(user.id)}
            Loading
        {:then times}
            <h3>Have a look at your times below:</h3>
            <table>
                <tr>
                    <th>Date</th>
                    <th>Time In</th>
                    <th>Time Out</th>
                </tr>
                <tbody>
                    {#each times as entry}
                        <tr>
                            <td>{entry.date}</td>
                            <td>{translate_date(entry.time_in)}</td>
                            <td>{translate_date(entry.time_out)}</td>
                        </tr>
                    {/each}
                </tbody>
            </table>
        {/await}
    {/await}
</div>

<style>
    table,
    th,
    tr,
    td {
        color: var(--text);
        text-align: center;
    }

    table tr {
        border-bottom: 1px solid #dddddd;
    }

    table td {
        padding: 10px;
    }

    table tbody tr:nth-of-type(odd) {
        background-color: var(--secondary);
        color: var(--primary);
    }

    table tbody tr:hover {
        background: var(--midpoint);
        transition: 0.2s;
    }

    h3 {
        color: var(--text);
    }
</style>
