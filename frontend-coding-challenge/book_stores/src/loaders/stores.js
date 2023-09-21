import apiClient from '../api';
import normalizeRelationships from './normalizers/relationships';
import normalizeStore from './normalizers/stores';

const getStores = async () => {
    const response = await apiClient.get('/stores')
    const data = response.data;
    const relIncludedData = normalizeRelationships(data.data, data.included);
    const normalizedData = relIncludedData.map(store => normalizeStore(store));
    return normalizedData;
}

export {getStores};