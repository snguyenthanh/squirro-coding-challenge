const getPopularBooksForStores = async (stores, limit = 2) => {
    if (!stores) return [];

    return stores.map(store => {
        const booksForStore = store.relationships?.books?.data || [];
        return (
            booksForStore.sort(
                (bookA, bookB) => bookB.attributes.copiesSold - bookA.attributes.copiesSold
            ).slice(0, limit)
        );
    });
}


export {getPopularBooksForStores};