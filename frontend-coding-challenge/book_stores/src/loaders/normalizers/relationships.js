const injectResourcesToRelationships = (relationships, includedResources) => {
    if (!relationships) return;

    for (const [resourceSingularType, rel] of Object.entries(relationships)) {
        if (Array.isArray(rel.data)) {
            rel.data = rel.data.map(relItem => ({
                ...relItem,
                attributes: includedResources[relItem.type][relItem.id].attributes,
                relationships: includedResources[relItem.type][relItem.id].relationships,
            }))
        }
        else {
            rel.data = {
                ...rel.data,
                attributes: includedResources[rel.data.type][rel.data.id].attributes,
                relationships: includedResources[rel.data.type][rel.data.id].relationships,
            }
        }
    }
}

const normalizeRelationships = (data, included) => {
    const includedResources = {};
    included.forEach(resource => {
        if (!(resource.type in includedResources)) includedResources[resource.type] = {};

        includedResources[resource.type][resource.id] = resource;
    });

    for (const resourceType in includedResources) {
        for (const [resourceId, resource] of Object.entries(includedResources[resourceType])) {
            if (resource.relationships) {
                injectResourcesToRelationships(
                    resource.relationships,
                    includedResources,
                );
            }
        }
    }

    data.forEach(item => {
        injectResourcesToRelationships(
            item.relationships,
            includedResources,
        );
    });

    return data;
};

export default normalizeRelationships;