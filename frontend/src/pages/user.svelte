<script>
    import axios from "axios";
    import { get } from "svelte/store";
    let showModal = false;
    let login = true;

    let user_list = [];
    let team_list = [];
    console.log(user_list);

    const get_users = async () => {
        await axios
            .get(`http://localhost:8000/users`)
            .then((res) => (user_list = res.data));
    };

    const get_teams = async () => {
        await axios
            .get(`http://localhost:8000/teams`)
            .then((res) => (team_list = res.data));
    };

    const toggleModal = async () => {
        await get_teams();
        showModal = !showModal;
    };

    const toggleLogin = async () => {
        login = !login;
    };

    const onSubmit = async (e) => {
        const formData = new FormData(e.target);

        const data = {};
        for (let field of formData) {
            const [key, value] = field;
            data[key] = value;
        }
        console.log(data);
        await axios
            .post(`http://localhost:8000/user`, {
                username: data.username,
                teamID: data.teamname,
                hasAdmin: data.hasAdmin,
            })
            .then((res) => console.log(res));
    };

    let current_user;
</script>

<div class="page">
    <div class="page-title">User</div>
    <div class="content-container">
        <div class="content">
            {#if current_user}
                You are currently logged in as: {current_user}
                <button on:click={() => toggleModal()}>Change User</button>
            {:else}
                You are not currently logged in.
                <button on:click={() => toggleModal()}> Log in </button>
            {/if}
        </div>
        <div class="content">
            <button on:click={() => get_users()}> Get Users </button>
        </div>
        <div class="content">
            {#each user_list as user}
                <p>
                    {user.username}
                </p>
            {/each}
        </div>
    </div>
    {#if showModal}
        <div class="modal-container" />
        <div class="modal-window">
            <button class="close" on:click={() => toggleModal()}>X</button>
            {#if login}
                <div class="page-title">Log In</div>
                <div class="form-container">
                    <form on:submit|preventDefault={onSubmit}>
                        <label for="username">Username</label>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                        />

                        <label for="password">Password</label>
                        <input
                            type="password"
                            name="password"
                            placeholder="Password"
                        />
                        <input class="end" type="submit" value="Submit" />
                    </form>
                    <br />
                    <div class="content bottom">
                        Want to create a new user?
                        <button on:click={() => toggleLogin()}>
                            Create User</button
                        >
                    </div>
                </div>
            {:else}
                <div class="page-title">Create User</div>
                <div class="form-container">
                    <form on:submit|preventDefault={onSubmit}>
                        <label for="username">Username</label>
                        <input
                            type="text"
                            name="username"
                            placeholder="Username"
                        />

                        <label for="hasAdmin">Admin? </label>
                        <select name="hasAdmin" id="hasAdmin">
                            <option value="true">true</option>
                            <option selected="selected" value="false">
                                false
                            </option>
                        </select>

                        <label for="teamname">Team Name</label>
                        <select name="teamname" id="teamname">
                            {#each team_list as team}
                                <option value={team.id}>{team.teamname}</option>
                            {/each}
                        </select>

                        <input class="end" type="submit" value="Submit" />
                    </form>
                    <br />
                    <div class="content bottom">
                        Already have an account?
                        <button on:click={() => toggleLogin()}> Log In</button>
                    </div>
                </div>
            {/if}
        </div>
    {/if}
</div>

<style>
    .content {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5%;
    }

    .modal-container {
        top: 0;
        left: 0;
        width: 100%;
        height: 110%;
        position: absolute;
        background: black;
        opacity: 0.5;
        animation: semifadein 0.5s;
        -webkit-animation: semifadein 0.5s;
    }
    .modal-window {
        top: 0;
        left: 0;
        transform: translate(20%, 20%);
        width: 60%;
        height: 60%;
        position: absolute;
        background: var(--secondary);
        border-radius: 20px;
        padding: 5%;
        animation: fadein 0.5s;
        -webkit-animation: fadein 0.5s;
    }
    .close {
        justify-self: end;
        font-family: monospace;
        float: right;
        width: 30px;
        height: 30px;
    }

    .form-container {
        background: #ffffff;
        width: 90%;
        height: inherit;
        padding: 5%;
        border-radius: 20px;
        display: flex;
        flex-direction: column;
    }

    form {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .end {
        align-self: end;
    }

    .bottom {
        padding-top: 10px;
    }

    @keyframes fadein {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    @keyframes semifadein {
        from {
            opacity: 0;
        }
        to {
            opacity: 0.5;
        }
    }
</style>
