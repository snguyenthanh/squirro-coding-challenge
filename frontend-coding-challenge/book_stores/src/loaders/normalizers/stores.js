import { format } from 'date-fns';

const normalizeStore = (store) => {
    const storeData = store.attributes;
    const establishmentDate = Date.parse(storeData.establishmentDate);
    storeData.establishmentDate = format(establishmentDate, 'dd.MM.yyyy');

    return store;
}


export default normalizeStore;