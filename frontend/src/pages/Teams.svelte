<script>
    import axios from "axios";
    import Warning from "../components/warning.svelte";
    import Icon from "@iconify/svelte";
    import { current_user_id } from "../store";
    import { get } from "svelte/store";

    let team_list = [];
    let response = [];
    let showAlert = false;
    let timer;
    $: if (response) {
        clearTimeout(timer);
        showAlert = true;
        timer = setTimeout(() => {
            showAlert = false;
        }, 3000);
    }

    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/team`)
            .then((res) => (team_list = res.data));

        return team_list;
    };

    const delete_team = async (teamID) => {
        if (await check_admin()) {
            await axios
                .delete(`http://localhost:8000/team/${teamID}`)
                .then(() => (response = ["Success", "Team Deleted"]));
            window.location.reload();
        } else {
            response = ["Error", "You do not have admin priveledges."];
        }
    };

    const check_admin = async () => {
        let userID = get(current_user_id);
        let hasAdmin = false;
        await axios
            .get(`http://localhost:8000/user/${userID}`)
            .then((res) => console.log(res.data));
        return hasAdmin;
    };

    const onSubmit = async (e) => {
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }
        try {
            await axios
                .post(`http://localhost:8000/team`, {
                    teamname: data.teamname,
                })
                .then(
                    () => (response = ["Success", "Team Successfully Created"])
                );
            window.location.reload();
        } catch (error) {
            response = ["Error", error.response.data.detail];
        }
    };
</script>

<div class="page">
    <div class="page-title">Teams</div>
    <div class="content-container">
        <div class="container-title">Teams</div>
        <div class="content">
            {#if response[0]}
                {#if showAlert}
                    <Warning>{response[1]}</Warning>
                {/if}
            {/if}
            <div class="formContainer" />
            <form on:submit|preventDefault={onSubmit}>
                <input name="teamname" placeholder="Team Name" type="text" />
                <input type="submit" value="Create new team" />
            </form>
            {#await get_teams()}
                Loading...
            {:then team_list}
                {#each team_list as team}
                    <div class="team-header">
                        {team.teamname}
                        <button
                            class="deleteButton"
                            on:click={() => delete_team(team.id)}
                        >
                            <Icon icon="ion:trash-bin-sharp" />
                        </button>
                    </div>
                    {#if team.users.length == 0}
                        There are no users in this team.
                    {:else}
                        <table>
                            <tr>
                                <th>Username</th>
                                <th>Role</th>
                            </tr>
                            <tbody>
                                {#each team.users as user}
                                    <tr>
                                        <td>
                                            {user.username}
                                        </td>
                                        <td>
                                            {#if user.hasAdmin}
                                                Admin
                                            {:else}
                                                User
                                            {/if}
                                        </td>
                                    </tr>
                                {/each}
                            </tbody>
                        </table>
                    {/if}
                {/each}
            {/await}
        </div>
    </div>
</div>

<style>
    .team-header {
        margin: 20px;
        color: var(--text);
        text-transform: capitalize;
        font-size: 32px;
        font-weight: 100;
        display: flex;
        flex-direction: row;
        gap: 15px;
        align-items: center;
    }

    table {
        text-align: center;
    }

    .formContainer {
        display: flex;
        flex-direction: row;
    }
</style>
