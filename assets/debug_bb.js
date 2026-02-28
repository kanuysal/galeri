rent && n.parent.isBone ? (n.matrix.copy(n.parent.matrixWorld).invert(), n.matrix.multiply(n.matrixWorld)) : n.matrix.copy(n.matrixWorld), n.matrix.decompose(n.position, n.quaternion, n.scale)) } } 
	refreshProducts() {
		this.cadres.forEach(c => c.destroy());
		this.btns.forEach(b => b.destroy());
		this.links.forEach(l => l.destroy());
		this.cadres = [];
		this.btns = [];
		this.links = [];
		this.articles = this.experience.router.articles;
		this.size = this.articles.length * 1.2 + 12;
		this.articles.forEach((t, n) => {
			const i = new th(new P(1.2 + n * 1.2, .99 + n % 2 * .99, -.5), new P(0, 0, 0), 1.5, this.experience.ressources.items[t.uid], t.uid),
				s = new dc(i.instance),
				o = new Sb(i.instance, s, t);
			this.cadres.push(i), this.btns.push(s), this.links.push(o)
		});
		if (this.roomGroup) {
			this.scene.remove(this.roomGroup);
			this.setRoom();
		}
		if (this.p1) {
			[this.p1, this.p2, this.p3, this.p4].forEach(p => { 
                if(p) { this.scene.remove(p); if(p.geometry) p.geometry.dispose(); if(p.material) p.material.dispose(); }
            });
			this.setPanneaux();
		}
	}
 update() { const e = this.bones, t = this.boneInverses, n = this.boneMatrices, i = this.boneTexture; for (let s = 0, o = e.length; s < o; s++) { const a = e[s] ? e[s].matrixWorld : Ly; Ou.multiplyMatrices(a, t[s]), Ou.toArray(n, s * 16) } i !== null && (i.needsUpdate = !0) } clone() { return new Rc(this.bones, this.boneInverses) } computeBoneTexture() { let e = Math.sqrt(this.bones.length * 4); e = cf(e), e = Math.max(e, 4); const t = new Float32Array(e * e * 4); t.set(this.boneMatrices); const n = new Tf(t, e, e, fn, wn); return n.needsUpdate = !0, this.boneMatrices = t, this.boneTexture = n, this.boneTextureSize = e, this } getBoneByName(e) { for (let t = 0, n = this.bones.length; t < n; t++) { const i = this.bones[t]; if (i.name === e) return i } } dispose() { this.boneTexture !== null && (this.boneTexture.dispose(), this.boneTexture = null) } fromJSON(e, t) { this.uuid = e.uuid; for (let n = 0, i = e.bones.length; n < i; n++) { const s = e.bones[n]; let o = t[s]; o === void 0 && (console.warn("THREE.Skeleton: No bone found with UUID:", s), o = new Af), thi