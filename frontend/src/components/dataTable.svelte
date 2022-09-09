<script>
    export let data = [];

    let flipped = false;
</script>

{#if flipped}
    <div class="container flipped" on:click={() => (flipped = !flipped)}>
        {#if data[1].id == "Empty"}
            <p>No data in this table.</p>
        {:else}
            <table>
                <tr>
                    <th>{data[0]}</th>
                </tr>
                <tr>
                    {#each Object.keys(data[1]) as key}
                        <th>{key}</th>
                    {/each}
                </tr>
                <tbody>
                    {#each data as row}
                        {#if row !== data[0]}
                            {#if row.id == "Empty"}
                                No data in this table.
                            {:else}
                                <tr>
                                    {#each Object.values(row) as val}
                                        {#if val == null}
                                            <td>{val}</td>
                                        {:else if typeof val == "object"}
                                            <td>{JSON.stringify(val)}</td>
                                        {:else}
                                            <td>{val}</td>
                                        {/if}
                                    {/each}
                                </tr>
                            {/if}
                        {/if}
                    {/each}
                </tbody>
            </table>
        {/if}
    </div>
{:else}
    <div class="container" on:click={() => (flipped = !flipped)}>
        <table>
            <tr>
                <th>{data[0]}</th>
            </tr>
            <tbody>
                {#if data[1]}
                    {#each Object.keys(data[1]) as key}
                        {#if key !== "header"}
                            <tr>
                                <td>{key}</td>
                            </tr>
                        {/if}
                    {/each}
                {/if}
            </tbody>
        </table>
    </div>
{/if}

<style>
    th {
        height: 60px;
    }
    .container {
        width: 100%;
        border-style: solid;
        border-width: 2px;
        border-color: #333;
        border-radius: 5px;
        /* margin-top: 20px; */
        transition: 0.2s;
    }
    .container:hover {
        background: var(--alt-primary);
    }

    .flipped {
        position: absolute;
        width: 80%;
        min-height: 300px;
        background: var(--primary);
    }

    p {
        color: var(--text);
    }

    td {
        max-width: 25px;
        overflow: hidden;
    }
    td:hover {
        max-width: fit-content;
    }
</style>
