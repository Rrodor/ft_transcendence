export function addBox(scn, pos, sze, col)
{
	// Create a box geometry
	const geometry = new THREE.BoxGeometry(sze.x, sze.y, sze.z);

	// Create a material
	const material = new THREE.MeshPhongMaterial({ color: col });

	// Create a mesh
	const mesh = new THREE.Mesh(geometry, material);

	// Add mesh to scene
	scn.add(mesh);

	mesh.position.set(pos.x, pos.y, pos.z);

	return { mesh };
}
