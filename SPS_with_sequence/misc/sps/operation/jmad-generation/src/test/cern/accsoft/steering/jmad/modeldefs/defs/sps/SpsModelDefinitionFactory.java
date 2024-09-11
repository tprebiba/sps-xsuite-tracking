/**
 * 
 */
package cern.accsoft.steering.jmad.modeldefs.defs.sps;

import java.util.HashSet;
import java.util.Set;

import cern.accsoft.steering.jmad.domain.file.CallableModelFile.ParseType;
import cern.accsoft.steering.jmad.domain.file.CallableModelFileImpl;
import cern.accsoft.steering.jmad.domain.file.ModelFile.ModelFileLocation;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsets;
import cern.accsoft.steering.jmad.domain.file.ModelPathOffsetsImpl;
import cern.accsoft.steering.jmad.domain.machine.RangeDefinitionImpl;
import cern.accsoft.steering.jmad.domain.machine.SequenceDefinitionImpl;
import cern.accsoft.steering.jmad.domain.twiss.TwissInitialConditionsImpl;
import cern.accsoft.steering.jmad.modeldefs.ModelDefinitionFactory;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.JMadModelDefinitionImpl;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinition;
import cern.accsoft.steering.jmad.modeldefs.domain.OpticsDefinitionImpl;

/**
 * This class is the implementation of the model definition for the Sps
 * 
 * @author Kajetan Fuchsberger (kajetan.fuchsberger at cern.ch)
 */
public class SpsModelDefinitionFactory implements ModelDefinitionFactory {

    private void addInitFiles(JMadModelDefinitionImpl modelDefinition) {
        /* beam */
//        modelDefinition
//                .addInitFile(new CallableModelFileImpl("beams/beam_lhc_injection.madx", ModelFileLocation.REPOSITORY));

        /* sequence */
        modelDefinition.addInitFile(new CallableModelFileImpl("SPS_LS2_2020-05-26.seq", ModelFileLocation.REPOSITORY));
    }

    private ModelPathOffsets createModelPathOffsets() {
        ModelPathOffsetsImpl offsets = new ModelPathOffsetsImpl();
        // offsets.setResourceOffset("sps");
        // offsets.setRepositoryOffset("sps/2014");
        offsets.setRepositoryPrefix("../");
        offsets.setResourcePrefix(".");
        return offsets;
    }

    private Set<OpticsDefinition> createOpticsDefinitions() {
        Set<OpticsDefinition> definitionSet = new HashSet<>();
        definitionSet.add(new OpticsDefinitionImpl("SPS-LHC-Q26-2021v1", new CallableModelFileImpl(
                "strengths/lhc_q26.str", ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("beams/beam_lhc_injection.madx", ModelFileLocation.REPOSITORY)));
        definitionSet.add(new OpticsDefinitionImpl("SPS-FT-Q26-2021v1", new CallableModelFileImpl(
                "strengths/ft_q26.str", ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("beams/beam_fixedtarget_injection.madx", ModelFileLocation.REPOSITORY)));
        definitionSet.add(new OpticsDefinitionImpl("SPS-LHC-Q20-2021v1", new CallableModelFileImpl(
                "strengths/lhc_q20.str", ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("beams/beam_lhc_injection.madx", ModelFileLocation.REPOSITORY)));

        definitionSet.add(new OpticsDefinitionImpl("SPS-LHC-Q22-2021v1", new CallableModelFileImpl(
                "strengths/lhc_q22.str", ModelFileLocation.REPOSITORY, ParseType.STRENGTHS),
                new CallableModelFileImpl("beams/beam_lhc_injection.madx", ModelFileLocation.REPOSITORY)));
        return definitionSet;
    }

    @Override
    public JMadModelDefinition create() {
        JMadModelDefinitionImpl modelDefinition = new JMadModelDefinitionImpl();

        modelDefinition.setName("SPS");
        modelDefinition.setModelPathOffsets(createModelPathOffsets());

        this.addInitFiles(modelDefinition);

        for (OpticsDefinition opticsDefinition : createOpticsDefinitions()) {
            modelDefinition.addOpticsDefinition(opticsDefinition);
            if (opticsDefinition.getName().equals("SPS-FT-Q26-2021v1"))
                modelDefinition.setDefaultOpticsDefinition(opticsDefinition);
        }

        /*
         * SEQUENCE
         */
        SequenceDefinitionImpl sps = new SequenceDefinitionImpl("sps", null);
        modelDefinition.setDefaultSequenceDefinition(sps);

        TwissInitialConditionsImpl twiss = new TwissInitialConditionsImpl("default-twiss");
        // twiss.setAlfx(alfx);
        twiss.setCalcAtCenter(true);
        twiss.setCalcChromaticFunctions(true);
        sps.setDefaultRangeDefinition(new RangeDefinitionImpl(sps, "ALL", twiss));

        return modelDefinition;
    }
}
