<script>
    import axios from "axios";
    import Icon from "@iconify/svelte";
    import { current_user_id } from "../store";

    export let alerts = [];
    let team_list = [];
    let target_user = 0;
    let current_user = $current_user_id;

    let showModal = false;

    const toggleModal = async (target) => {
        target_user = target;
        await get_teams();
        showModal = !showModal;
    };

    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/team`)
            .then((res) => (team_list = res.data));
    };

    get_teams();

    const check_admin = async () => {
        let userID = current_user;
        let hasAdmin = false;
        await axios
            .get(`http://localhost:8000/user/${userID}`)
            .then((res) => (hasAdmin = res.data.hasAdmin));
        return hasAdmin;
    };

    const delete_user = async (user_id) => {
        if (current_user == 0) {
            alerts.push(["Error", "You must be logged in to do this."]);
            alerts = alerts;
            return;
        }

        if (current_user == user_id) {
            alerts.push(["Error", "You can't delete yourself."]);
            alerts = alerts;
            return;
        }
        try {
            await axios
                .delete(
                    `http://localhost:8000/user/${user_id}?authUserID=${$current_user_id}`
                )
                .then(() => alerts.push(["Success", "User Deleted"]));
            alerts = alerts;
            get_teams();
        } catch (error) {
            alerts.push(["Error", error.response.data.detail]);
            alerts = alerts;
        }
    };

    const delete_team = async (teamID) => {
        if (!$current_user_id) {
            alerts.push(["Error", "You must be logged in to do this."]);
            alerts = alerts;
            return;
        }

        try {
            await axios
                .delete(
                    `http://localhost:8000/team/${teamID}?authUserID=${$current_user_id}`
                )
                .then(() => alerts.push(["Success", "Team Deleted"]));
            alerts = alerts;
            get_teams();
        } catch (error) {
            alerts.push(["Error", error.response.data.detail]);
            alerts = alerts;
        }
    };

    const create_team = async (e) => {
        const formData = new FormData(e.target);
        if (current_user == 0) {
            alerts.push(["Error", "You must be logged in to do this."]);
            alerts = alerts;
            return;
        }

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
                .then(() =>
                    alerts.push(["Success", "Team Successfully Created"])
                );
            alerts = alerts;
            get_teams();
        } catch (error) {
            alerts.push(["Error", error.response.data.detail]);
            alerts = alerts;
        }
    };

    const editUser = async (e) => {
        if (current_user == 0) {
            alerts.push(["Error", "You must be logged in to do this."]);
            alerts = alerts;
            return;
        }
        if (!check_admin($current_user_id)) {
            alerts.push(["Error", "You do not have admin priveleges."]);
            alerts = alerts;
            return;
        }
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }

        try {
            await axios
                .patch(`http://localhost:8000/user/${target_user}`, {
                    username: data.username,
                    hasAdmin: data.hasAdmin,
                    teamID: data.teamID,
                })
                .then(() =>
                    alerts.push(["Success", "User edited successfully"])
                );
            alerts = alerts;
            get_teams();
            toggleModal(0);
        } catch (error) {
            alerts.push(["Error", error.response.data.detail]);
            alerts = alerts;
        }
    };
    let editable = 0;
    const toggleEdit = (id) => {
        editable = id;
        alerts = alerts;
    };
    const editTeam = async (e) => {
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }

        try {
            await axios
                .patch(`http://localhost:8000/team/${editable}`, {
                    teamname: data.teamname,
                })
                .then(() => alerts.push(["Success", "Teamname Updated"]));
            alerts = alerts;
            get_teams();
            toggleEdit(0);
        } catch (error) {
            console.log(error);
            alerts.push(["Error", error.response.data.detail]);
            alerts = alerts;
        }
    };
</script>

<div class="page">
    <div class="page-title">Teams</div>
    <div class="content">
        <form on:submit|preventDefault={create_team}>
            <input name="teamname" placeholder="Team Name" type="text" />
            <input type="submit" value="Create new team" />
        </form>
        <p>
            View the current teams below. If you would like to change a team
            name, please double click the name.
        </p>

        {#each team_list as team}
            <div class="team-header" on:dblclick={() => toggleEdit(team.id)}>
                {#if editable == team.id}
                    <form on:submit|preventDefault={editTeam}>
                        <input
                            on:blur={() => toggleEdit("")}
                            autofocus
                            class="teamname-form"
                            name="teamname"
                            value={team.teamname}
                            type="text"
                        />
                    </form>
                {:else}
                    {team.teamname}
                {/if}
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
                        <th>Edit</th>
                        <th>Delete</th>
                    </tr>
                    <tbody>
                        {#each team.users as user}
                            <tr
                                class={user.id == $current_user_id
                                    ? "current"
                                    : ""}
                            >
                                <td>
                                    {user.username}
                                    <strong>
                                        {user.id == $current_user_id
                                            ? "(You)"
                                            : ""}
                                    </strong>
                                </td>
                                <td>
                                    {#if user.hasAdmin}
                                        Admin
                                    {:else}
                                        User
                                    {/if}
                                </td>
                                <td class="small_column">
                                    <button
                                        on:click={() => toggleModal(user.id)}
                                        class="edit_button"
                                    >
                                        <Icon icon="bxs:edit" />
                                    </button>
                                </td>
                                <td class="small_column">
                                    <button
                                        on:click={() => delete_user(user.id)}
                                        class="deleteButton"
                                    >
                                        <Icon icon="ion:trash-bin-sharp" />
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    </tbody>
                </table>
            {/if}
        {/each}
    </div>
    {#if showModal}
        <div class="modal-container" />
        <div class="modal-window">
            <button class="close" on:click={() => toggleModal(0)}>X</button>
            <div class="page-title">Edit User</div>
            <div class="modalFormContainer">
                <form class="modalForm" on:submit|preventDefault={editUser}>
                    <label for="username">Username</label>
                    <input type="text" name="username" placeholder="Username" />
                    <!-- Change this to a switch -->
                    <label for="hasAdmin">Admin? </label>
                    <select name="hasAdmin" id="hasAdmin">
                        <option value="true">true</option>
                        <option selected="selected" value="false">
                            false
                        </option>
                    </select>

                    <label for="teamname">Team Name</label>
                    <select name="teamID" id="teamname">
                        {#each team_list as team}
                            <option value={team.id}>{team.teamname}</option>
                        {/each}
                    </select>

                    <input class="end" type="submit" value="Submit" />
                </form>
            </div>
        </div>
    {/if}
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

    .teamname-form {
        background: var(--primary);
        color: var(--text);
        text-transform: capitalize;
        font-size: 32px;
        font-weight: 100;
        width: fit-content;
        border: none;
    }
    .edit_button {
        font-size: 32px;
        background: none;
    }

    .small_column {
        width: 10%;
    }

    .end {
        align-self: end;
    }

    .current {
        background: var(--ternary);
    }

    .current:hover {
        background: var(--alt-ternary);
        animation: wash 0.2s ease-in-out forwards;
    }

    @keyframes wash {
        0% {
            background: var(--primary);
        }

        10% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 90%
            );
        }

        20% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 80%
            );
        }

        30% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 70%
            );
        }

        40% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 60%
            );
        }

        50% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 50%
            );
        }

        60% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 40%
            );
        }

        70% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 30%
            );
        }

        80% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 20%
            );
        }

        90% {
            background: linear-gradient(
                -90deg,
                var(--ternary),
                var(--alt-ternary) 10%
            );
        }

        100% {
            background: var(--alt-ternary);
        }
    }
</style>
