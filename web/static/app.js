let state = {
	presets: {},
	results: [],
	selectedPreset: null,
	file: null,
	autoScan: true,
}

const ui = {
	path: document.getElementById('path'),
	apis: document.getElementById('apis'),
	analyze: document.getElementById('analyzeBtn'),
	clear: document.getElementById('clearBtn'),
	results: document.getElementById('results'),
	summary: document.getElementById('summary'),
	error: document.getElementById('errorBox'),
	chips: document.getElementById('chips'),
	filePicker: document.getElementById('filePicker'),
	browse: document.getElementById('browseBtn'),
	dropZone: document.getElementById('dropZone'),
	savePreset: document.getElementById('savePresetBtn'),
}

function setSelectedFile(file) {
	if (!file) return

	state.file = file
	ui.path.value = `${file.name} (${Math.round(file.size / 1024)} KB)`
	ui.dropZone.classList.add('has-file')

	// автоскан
	if (state.autoScan) {
		runAnalyze()
	}
}

function bindFileControls() {
	ui.browse.addEventListener('click', () => {
		ui.filePicker.click()
	})

	ui.filePicker.addEventListener('change', () => {
		const file = ui.filePicker.files[0]
		setSelectedFile(file)
	})
	;['dragenter', 'dragover'].forEach(eventName => {
		ui.dropZone.addEventListener(eventName, e => {
			e.preventDefault()
			e.stopPropagation()
			ui.dropZone.classList.add('dragover')
		})
	})
	;['dragleave', 'dragend', 'drop'].forEach(eventName => {
		ui.dropZone.addEventListener(eventName, e => {
			e.preventDefault()
			e.stopPropagation()
			ui.dropZone.classList.remove('dragover')
		})
	})

	ui.dropZone.addEventListener('drop', e => {
		const file = e.dataTransfer.files[0]
		if (!file) return

		setSelectedFile(file)
	})
}

async function loadPresets() {
	const res = await fetch('/static/presets.json')
	state.presets = await res.json()
}

function renderPresets() {
	const container = document.getElementById('chips')
	container.innerHTML = ''

	Object.entries(state.presets).forEach(([key, preset]) => {
		const btn = document.createElement('button')
		btn.className = 'chip'
		btn.dataset.preset = key
		btn.innerText = preset.title || key

		btn.addEventListener('click', () => {
			// снять выделение со всех
			container.querySelectorAll('.chip').forEach(b => {
				b.classList.remove('active')
			})

			// поставить активный
			btn.classList.add('active')

			// сохранить состояние
			state.selectedPreset = key

			// вставить API
			ui.apis.value = preset.apis.join('\n')
		})

		btn.addEventListener('contextmenu', async e => {
			e.preventDefault()

			const confirmDelete = confirm(`Delete preset "${preset.title || key}"?`)
			if (!confirmDelete) return

			const res = await fetch('/api/presets/delete', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ key }),
			})

			const data = await res.json()

			if (data.error) {
				return fail(data.error)
			}

			// обновить UI
			await loadPresets()
			renderPresets()

			ui.summary.textContent = `Preset "${preset.title}" deleted`
		})

		container.appendChild(btn)
	})
}

function copyText(btn, text) {
	if (btn.classList.contains('copying') || btn.classList.contains('copied')) {
		return
	}

	navigator.clipboard.writeText(text)

	btn.classList.add('copying')

	setTimeout(() => {
		btn.classList.remove('copying')
		btn.classList.add('copied')

		const original = btn.innerText
		btn.innerText = `✔ ${text.slice(0, 10)}`

		setTimeout(() => {
			btn.classList.remove('copied')
			btn.innerText = original
		}, 1200)
	}, 150)
}

function setError(text) {
	if (!text) {
		ui.error.classList.add('hidden')
		return
	}

	ui.error.textContent = text
	ui.error.classList.remove('hidden')
}

function fail(msg) {
	setError(msg)
	ui.summary.textContent = 'Analysis failed'
}

function renderCard(item) {
	const card = document.createElement('div')
	card.className = 'card'

	card.innerHTML = `
        <div class="card-header">
            <div class="card-title">${item.api}</div>
            <div class="${item.score >= 5 ? 'badge hot' : 'badge'}">
                score ${item.score.toFixed(3)}
            </div>
        </div>

        <div class="meta">
            ${metaItem('DLL', item.dll)}
            ${metaItem('VA', item.va)}
            ${metaItem('RVA', item.rva)}
            ${metaItem('.text offset', item.offset)}
        </div>

        <div class="card-actions">
            <button class="small-btn" data-copy="va">Copy VA</button>
            <button class="small-btn" data-copy="rva">Copy RVA</button>
            <button class="small-btn" data-copy="api">Copy API</button>
        </div>
    `

	card.querySelectorAll('[data-copy]').forEach(btn => {
		btn.addEventListener('click', () => {
			const type = btn.dataset.copy
			const value = item[type]

			copyText(btn, value)
		})
	})

	return card
}

function metaItem(label, value) {
	return `
        <div class="meta-item">
            <div class="meta-label">${label}</div>
            <div class="meta-value">${value}</div>
        </div>
    `
}

ui.apis.addEventListener('input', () => {
	if (state.selectedPreset) {
		state.selectedPreset = null

		document.querySelectorAll('.chip').forEach(b => {
			b.classList.remove('active')
		})
	}
})

async function runAnalyze() {
	setError('')
	ui.results.innerHTML = ''
	ui.summary.textContent = 'Analyzing...'

	const apis = ui.apis.value
		.split('\n')
		.map(x => x.trim())
		.filter(Boolean)

	if (!apis.length) return fail('Add at least one API.')

	try {
		const form = new FormData()

		if (state.file) {
			form.append('file', state.file)
		} else {
			const path = ui.path.value.trim()
			if (!path) return fail('Path or file is required.')
			form.append('path', path)
		}

		form.append('apis', JSON.stringify(apis))

		const res = await fetch('/api/analyze', {
			method: 'POST',
			body: form,
		})

		const data = await res.json()

		if (!res.ok || data.error) {
			throw new Error(data.error || 'Unknown error')
		}

		state.results = data.results
		ui.summary.textContent = `Found ${data.count} candidates`
		renderResults()
	} catch (err) {
		fail(err.message)
	}
}

function renderResults() {
	ui.results.innerHTML = ''

	if (!state.results.length) {
		ui.results.innerHTML = `<div class="card">No candidates</div>`
		return
	}

	state.results.forEach(r => {
		ui.results.appendChild(renderCard(r))
	})
}

ui.savePreset.addEventListener('click', async () => {
	const apis = ui.apis.value
		.split('\n')
		.map(x => x.trim())
		.filter(Boolean)

	if (!apis.length) {
		return fail('No APIs to save')
	}

	const name = prompt('Preset name:')
	if (!name) return

	const res = await fetch('/api/presets/save', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({
			name,
			apis,
		}),
	})

	const data = await res.json()

	if (data.error) {
		return fail(data.error)
	}

	// перезагрузить presets
	await loadPresets()
	renderPresets()
})

function clearAll() {
	ui.path.value = ''
	ui.apis.value = ''
	ui.results.innerHTML = ''
	ui.summary.textContent = 'No analysis yet'

	state.results = []
	state.selectedPreset = null
	state.file = null

	setError('')

	ui.chips.querySelectorAll('.chip').forEach(btn => {
		btn.classList.remove('active')
	})
}

async function init() {
	await loadPresets()
	renderPresets()
	bindFileControls()

	ui.analyze.addEventListener('click', runAnalyze)
	ui.clear.addEventListener('click', () => {
		clearAll()
	})
	ui.browse.addEventListener('click', () => {
		ui.filePicker.click()
	})

	ui.filePicker.addEventListener('change', () => {
		const file = ui.filePicker.files[0]
		if (!file) return

		state.file = file

		// показываем имя + размер
		ui.path.value = `${file.name} (${Math.round(file.size / 1024)} KB)`
	})
}

init()
