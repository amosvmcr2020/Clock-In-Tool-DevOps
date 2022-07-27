<script>
    import { Link } from "svelte-navigator";

    import { fly } from "svelte/transition";

    export let show;
</script>

{#if show}
    <div transition:fly={{ x: 250, opacity: 1 }}>
        <h1>Menu</h1>
        <Link to="/">Home</Link>
        <Link to="teams">Teams</Link>
        <h4>Change User</h4>
        <p>blah blah blah</p>
    </div>
{/if}

<style>
    div {
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: fixed;
        top: 0;
        right: 0;
        height: 100%;
        padding: 2rem 1rem 0.6rem;
        border-left: 1px solid #aaa;
        background: #fff;
        overflow-y: auto;
        width: 10rem;
    }
</style>
