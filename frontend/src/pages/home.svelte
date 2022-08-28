<script>
    import axios from "axios";
    import { get } from "svelte/store";
    import { current_user_id } from "../store";
    import { Link } from "svelte-navigator";
    import ClockIn from "./clock-in.svelte";

    let user;
    let times = [];

    export let alerts;

    const get_timesheet = async (user_id) => {
        await axios
            .get(`http://localhost:8000/user/${user_id}/timesheet/summary`)
            .then((res) => (times = res.data.times));
        return times;
    };

    const get_current_user = async () => {
        await axios
            .get(`http://localhost:8000/user/${get(current_user_id)}`)
            .then((res) => (user = res.data));
        return user;
    };

    const translate_date = (date_str) => {
        if (date_str == null) {
            return "";
        }
        let date = new Date(date_str);
        date = date.toLocaleTimeString();
        return date;
    };
</script>

<div class="page">
    {#if get(current_user_id) == 0}
        <div class="page-title">Hello!</div>
        <div class="msgContainer">
            <p>You are not currently logged in. Please log in</p>
            <Link to="/user">here</Link>
        </div>
    {:else}
        {#await get_current_user()}
            Loading
        {:then user}
            <div class="page-title">Hello {user.username}!</div>
            {#await get_timesheet(user.id)}
                Loading
            {:then times}
                <ClockIn bind:alerts />
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
    {/if}
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

    p,
    h3 {
        color: var(--text);
    }

    .msgContainer {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 5px;
    }
</style>
